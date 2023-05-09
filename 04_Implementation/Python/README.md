# Python Implementation

## Requirements
### Python (v3.10.0)
Install Python by downloading and installing the setup from https://www.python.org/downloads/

### Libraries
```
pip install pandas Pillow tk matplotlib
```

### Files needed and where to keep them
- **main.py** in ```...\Python```
- **processing.py** in ```...\Python```
- **graphics.py** in ```...\Python```
- **graphicsCalculations.py** in ```...\Python```
- **tools.py** in ```...\Python```
- **heatmap.py** in ```...\Python```
- **donutchart.py** in ```...\Python```
- **config.txt** has to be copied to ```...\c++\x64\Debug```
- **C++.exe** in ```...\c++\x64\Debug``` after compiling once
- **csvdata.csv** will be created in ```...\c++\x64\Debug```

**IMPORTANT:** Files in the ```...\c++``` directory have to be created by compiling and building once with Visual Studio.
C (haha) the C++ part of this repository for more information.

### Eyetracker or csvdata.csv
To have any form of output or success you will either need to
- Set ```PY_APPLICATION_MODE=DEV``` (in config.txt) and supply a csvdata.csv as stated above.
- Set ```PY_APPLICATION_MODE=NORMAL``` (in config.txt) and have a Tobii 5 Eyetracker intalled and connected.

## Usage
### Start
Navigate your terminal to this folder:
```
...\uas-ss-22-eye-tracking-video-meeting\04_Implementation\Python
```
and execute the command
```
python main.py
```