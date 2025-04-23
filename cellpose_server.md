# Start Cellpose Server
## Description
Starts Cellpose Server locally to allow fast calling Cellpose segmentation without relaunching Python environment for every image (sets).
Start Cellpose Server once in a session when you start to work, and leave the command window open as long as it is needed. 
To stop Cellpose Server, close the command window.

The server will be available at: http://localhost:5001/segment
The field names for the API call match the parameters of the command line Cellpose, therefore Image Analyst MKII pipelines previously using command line launching Cellpose can be simply switched to using the Cellpose server by replacing in the “Path and filename or URL (*.exe,*.bat,"command && command")”  parameter:

=""%ProgramDataFolder%cellpose\Scripts\activate"  && "python.exe""

With

http://localhost:5001/segment

Command line parameters translated by cellpose_server.py:
--dir
--pretrained_model
--diameter
--chan
--chan2
--cellprob_threshold
--flow_threshold
--batch_size

By default, cellpose_server.py is configured to run Cellpose on GPU.
Image data is transferred through a temporary folder, similarly to the command line operation of Cellpose.


## Parameters
| # | Name | Type | Description |
|---|------|------|-------------|


## Structure
![structure](/img/cellpose_server.jpg)

[Image Analyst MKII](https://www.imageanalyst.net) pipeline - saved by V4.3.2 (build 999)

