# Starts Cellpose Server locally to allow fast calling Cellpose segmentation without relaunching Python environment for every image (sets).
# The server will be available at: http://127.0.0.1:5001/segment

from flask import Flask, request, jsonify
from cellpose import models
import numpy as np
import imageio.v2 as imageio
import glob
import os
from concurrent.futures import ThreadPoolExecutor
import threading
from queue import Queue
import argparse

app = Flask(__name__)
threadcount = 5
model_pool = Queue()
current_model_type = None
pool_lock = threading.Lock()

def initialize_model_pool(model_type):
    """Initialize a pool of models for multithreading"""
    global model_pool, current_model_type
    
    # Clear existing pool
    while not model_pool.empty():
        try:
            model_pool.get_nowait()
        except:
            break
    
    # Create new pool with the requested model type
    print(f"Initializing {threadcount} models of type: {model_type}")
    for i in range(threadcount):
        model = models.Cellpose(gpu=True, model_type=model_type)
        model_pool.put(model)
        print(f"Model {i+1}/{threadcount} initialized")
    
    current_model_type = model_type

def process_single_image(img_path_single, model_params):
    """Process a single image with its own dedicated model"""
    try:
        # Get a model from the pool
        model = model_pool.get()
        
        try:
            # Read the image
            img = imageio.imread(img_path_single)
            
            # Use the model (no locking needed - each thread has its own model)
            masks, flows, styles, diams = model.eval(
                img,
                batch_size=model_params['batch_size'],
                diameter=model_params['diameter'],
                channels=[model_params['chan'], model_params['chan2']],
                cellprob_threshold=model_params['cellprob_threshold'],
                flow_threshold=model_params['flow_threshold'],
                resample=False
            )
            
            # Save the result
            save_path = img_path_single.replace(".tif", "_cp_masks.tif").replace(".jpg", "_cp_masks.tif")
            imageio.imwrite(save_path, masks.astype(np.uint16))
            
            return {"status": "success", "image": img_path_single, "save_path": save_path}
            
        finally:
            # Always return the model to the pool
            model_pool.put(model)
            
    except Exception as e:
        return {"status": "error", "image": img_path_single, "error": str(e)}

@app.route('/segment', methods=['POST'])
def segment():
    global current_model_type
    
    print('Segmenting')
    print(request.form)
    img_path = request.form['--dir']
    
    # Get requested model name from user
    requested_model = str(request.form.get('--pretrained_model', 'cyto3'))  # default to 'cyto3'
    
    # Check if we need to reinitialize the model pool
    with pool_lock:
        if current_model_type != requested_model:
            initialize_model_pool(requested_model)

    # Parse the rest of the request parameters
    model_params = {
        'batch_size': int(request.form.get('--batch_size', 64)),
        'diameter': float(request.form.get('--diameter', 40)),
        'chan': int(request.form.get('--chan', '0')),
        'chan2': int(request.form.get('--chan2', '0')),
        'cellprob_threshold': float(request.form.get('--cellprob_threshold', 0)),
        'flow_threshold': float(request.form.get('--flow_threshold', 0))
    }
    
    # Check if the img_path contains common wildcard characters.
    if any(ch in img_path for ch in "*?[]"):
        # Use glob to match the pattern.
        img_list = glob.glob(img_path)
    else:
        # If no wildcard is found, check if the folder of file exists.
        if os.path.isdir(img_path):
            img_list = glob.glob(img_path+'*.tif')
            img_list.extend(glob.glob(img_path+'*.jpg'))
        elif os.path.isfile(img_path):
            img_list = [img_path]
        else:
            return jsonify({"status": "failed", "mask_path": ""})

    print(f"Processing {len(img_list)} images with {threadcount} threads")
    print(img_list)
    
    # Process images using ThreadPoolExecutor
    results = []
    failed_images = []
    last_save_path = ""
    
    with ThreadPoolExecutor(max_workers=threadcount) as executor:
        # Submit all tasks
        future_to_image = {
            executor.submit(process_single_image, img_path_single, model_params): img_path_single 
            for img_path_single in img_list
        }
        
        # Collect results as they complete
        for future in future_to_image:
            result = future.result()
            results.append(result)
            
            if result["status"] == "success":
                last_save_path = result["save_path"]
                print(f"Successfully processed: {result['image']}")
            else:
                failed_images.append(result["image"])
                print(f"Failed to process: {result['image']} - Error: {result['error']}")
    
    # Prepare response
    if failed_images:
        return jsonify({
            "status": "partial_success" if len(failed_images) < len(img_list) else "failed",
            "mask_path": last_save_path,
            "processed": len(img_list) - len(failed_images),
            "total": len(img_list),
            "failed_images": failed_images
        })
    else:
        return jsonify({
            "status": "done", 
            "mask_path": last_save_path,
            "processed": len(img_list),
            "total": len(img_list)
        })

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Flask Cellpose Segmentation Server')
    parser.add_argument('--threadcount', type=int, default=5, 
                       help='Number of threads for concurrent processing (default: 5)')
    args = parser.parse_args()
    
    # Set the global threadcount from command line argument
    threadcount = args.threadcount
    print(f"Using {threadcount} threads for processing")

    # Initialize the model pool with default model on startup
    print("Initializing model pool...")
    initialize_model_pool('cyto3')
    print("Starting Flask server...")
    app.run(host='127.0.0.1', port=5001)