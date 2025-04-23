# Starts Cellpose Server locally to allow fast calling Cellpose segmentation without relaunching Python environment for every image (sets).
# The server will be available at: http://127.0.0.1:5001/segment


from flask import Flask, request, jsonify
from cellpose import models
import numpy as np
import imageio.v2 as imageio
import glob
import os

app = Flask(__name__)
prev_model = ""
model = None
@app.route('/segment', methods=['POST'])
def segment():
    global model
    global prev_model
    print('Segmenting')
    print(request.form)
    img_path = request.form['--dir']
    
    # Get requested model name from user
    requested_model = str(request.form.get('--pretrained_model', 'cyto3'))  # default to 'cyto3'
    
    
    # Check if the model matches the loaded model
    if (prev_model != requested_model) or not model:
        model = models.Cellpose(gpu=True, model_type=requested_model)  # Load once!
        prev_model = requested_model

    # Parse the rest of the request parameters
    batch_size = int(request.form.get('--batch_size', 64))
    diameter = float(request.form.get('--diameter', 40))
    chan = int(request.form.get('--chan', '0'))
    chan2 = int(request.form.get('--chan2', '0'))
    cellprob_threshold = float(request.form.get('--cellprob_threshold', 0))
    flow_threshold = float(request.form.get('--flow_threshold', 0))
    
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

    print(img_list)
    for img_path_single in img_list:
        img = imageio.imread(img_path_single)
        masks, flows, styles, diams = model.eval(
            img,
            batch_size=batch_size,
            diameter=diameter,
            channels=[chan, chan2],
            cellprob_threshold=cellprob_threshold,
            flow_threshold=flow_threshold,
            resample=False
        )

        save_path = img_path_single.replace(".tif", "_cp_masks.tif").replace(".jpg", "_cp_masks.tif")
        imageio.imwrite(save_path, masks.astype(np.uint16))
    return jsonify({"status": "done", "mask_path": save_path})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
