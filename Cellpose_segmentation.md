# Cellpose segmentation
## Description
This pipeline uses Cellpose to detect nuclei or cells in a single channel. The input image (series) is exported, processed by Cellpose 2.0 command line and results are imported. Image transfer is through a unique temp folder opened for each call, within the Image Export Folder. See Files/Set Folder Locations to set this. By default, these temporary folders are deleted, see switch in the Run EXE function. Use Cellpose GUI to fine tune thresholds. Start GUI in Pipelines/Using External Programs/Cellpose/Launch cellpose GUI. Save images to be loaded into the GUI use the Files/Export RGB Full Size Image, or by disabling temp folder deletion above, and locating the temp folder.

Input:
* Fluorescence images: these will be intensity rescaled, and optionally gamma corrected and denoised as preprocessing.
* Brightfield images: grayscale input; no intensity scaling or gamma are applied, optionally denoised. Some Cellpose models work well with bright field images (e.g. livecell) others don’t.
* Brightfield to be inverted: The pipeline will invert the grayscale brightfield image and scale it similarly as for fluorescence images.

Cellpose will run faster if the same number of images are processed as an image series than one-by-one. Further speed increment can be achieved by increasing batch size and number of parallel processes, depending on the available system memory and the image size. Use batch size of 64 and 4 parallel processes with 24GB GPU. Further command line options can be entered by editing this pipeline in the Run EXE function, Argument parameter. 

This pipeline uses Cellpose 2.0. Cellpose is installed by the user as given in the Image Analyst MKII Primer/TOC/Using external programs.

Pachitariu M, Stringer C. Cellpose 2.0: how to train your own model. Nat Methods. 2022;19(12):1634-41
https://github.com/MouseLand/cellpose

Keywords: U-Net, CNN, deep learning, generalist cell segmentation, artificial intelligence, AI

Version history
V2: Added fluorescence/brightfield selector, optional inversion and optional disabling of Wiener filtering.


## Parameters
| # | Name | Type | Description |
|---|------|------|-------------|
| 0 | Image type for intensity scaling | Text | Only fluorescence images are rescaled, brightfield ones are used as are. Inverted brightfield images will be rescaled. |
| 1 | Cells: Scale maximum (percentile) | Real | This percentile of the image histogram sets the intensity value where the maximum of the Look Up Table (LUT) is scaled. Use -1 to override this with fixed value set below at "Max value". |
| 2 | Cells: Gamma | Real | A gamma value >1 makes image supralinearly brighter, a gamma value <1 makes the image sublinearly darker. |
| 3 | Cells: Smooth factor | Real | Wiener filter noise level (0-1). Higher value provides more smoothing. Set zero for no smoothing. |
| 4 | Cells: Cellpose Model (pretrained network) | Text | Enter a pretrained model name from the model zoo, or name for user trained model installed into the GUI. See --pretrained_model option in Cellpose. |
| 5 | Cells: Cellpose Diameter (pixels) | Text | Approximate diameter of objects in pixels. Use 0 for auto detection of size for nuclei or cyto models only. |
| 6 | Cells: Cellpose --flow_threshold | Text | Maximum allowed error of the flows for each mask. A higher value (0-1) will allow more detection. |
| 7 | Cells: Cellpose --cellprob_threshold | Text | Minimum probability to return ROIs. A lower value will allow more detection. |
| 8 | Cells: Minimum size of cells (pixels area) | Integer | The result provided by Cellpose is gated for this minimum pixel area per object |
| 9 | Cells: Maximum size of cells (pixels area) | Integer | The result provided by Cellpose is gated for this minimum maximum area per object |
| 10 | Python.exe in the Cellpose Environment | Text | Prerequisite:Cellpose. Change environment name if needed. Syntax: Filename with full path, or filename only if it is in the environment path. Alternatively, use one or more command prompt expressions with arguments concatenated by && and the whole expression quoted with ". |
| 11 | Cellpose: number of parallel processes | Integer | Image series and time courses will be split into multiple parts and separate instances of the external program is launched. |
| 12 | Cellpose: --batch_size | Text | Set batch size according to the GPU memory and number of parallel processes. E.g. 3 parallel process (for series only) and 64 batch size with 24GB VRAM. |


## Structure
![structure](/img/Cellpose_segmentation.jpg)

[Image Analyst MKII](https://www.imageanalyst.net) pipeline - saved by V4.3.2 (build 999)

