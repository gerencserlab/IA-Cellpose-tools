# Cellpose Tools
This repository provides Cellpose Server for Image Analyst MKII. Cellpose Server allows fast calling Cellpose segmentation without relaunching Python environment for every image (series). This can be used with any Image Analyst MKII pipeline previously using command line launching, by replacing command line path and filename with the server URL (http://localhost:5001/segment).
[This repository](https://github.com/gerencserlab/IA-Cellpose-tools/) contains custom image analysis pipelines for Image Analyst MKII.    

## List of pipelines
* [Cellpose segmentation](Cellpose_segmentation.md)
* [Start Cellpose Server](cellpose_server.md)
* [Install Cellpose Server](install_cellpose_server.md)

## How to use
To open and edit *.ips (XML) Image Processing Pipeline files download [Image Analyst MKII for Windows](https://www.imageanalyst.net/downloads/?item=recent/imageanalystMKII64.msi).
1. Clone this git in Image Analyst MKII by Edit/Download and Manage Pipelines from GitHub. 
2. Press the "< > Code" button [above in this page](https://github.com/gerencserlab/IA-Cellpose-tools/) and copy the URL of this git.
3. Paste the URL in the URL field in the Connect to Git window in Image Analyst MKII.
4. Press Download.
5. The pipelines deposited here will appear in the middle section of the Pipelines main menu.
* Note: you may download individual pipelines and add them to the Documents\Image Analyst\My Pipelines

[Gerencser Lab on Github](https://github.com/gerencserlab)

