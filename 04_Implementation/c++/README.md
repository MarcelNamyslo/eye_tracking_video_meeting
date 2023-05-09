# C++ Implementation

## Requirements
### Visual Studio 2022 Community Edition
Go to https://visualstudio.microsoft.com/downloads/ to download and install the VS 2022 Community Edition.

### File locations and which to copy
- **config.txt** copy from ```...\c++``` to ```...\c++\x64\Debug```. Only if you want to execute the C++.exe directly (or through the Python application). If executed with the ```Local Windows Debugger``` button, you dont have to do this.
- **C++.exe** in ```...\c++\x64\Debug\```
- **csvdata.csv** will be created in ```...\c++\x64\Debug```. Or in ```...\c++``` if C++.exe was executed with the ```Local Windows Debugger``` button.

Files and folders in the ```...\c++\x64\Debug``` are created when you first time press the ```Local Windows Debugger``` button.

Also it is important to mention that when using ```Local Windows Debugger``` in VS 2022 you use/create the csvdata.csv and config.txt located in the top level ```...\c++``` folder. When executing the C++.exe from Python csvdata.csv and config.txt in ```...\c++\x64\Debug``` are used/created.

### Controll application flow
For more fine granular controll
- Set ```C_APPLICATION_MODE=DEV``` (in config.txt) to have more controll with keyboard buttons.
- Set ```C_APPLICATION_MODE=NORMAL``` (in config.txt) have everything work as usual.

## Usage
### Visual Studio Setup
Navigate your terminal to
```
...\uas-ss-22-eye-tracking-video-meeting\04_Implementation\c++
```
and open the ```C++.sln``` file. Visual Studio should open.

\
Under ```Project > C++ Properties``` check if the following settings are still existent

- ```Project > C++ Properties > C/C++ > General```
![/06_Resources/cpp-general.png](/06_Resources/Visual_Studio_Project_Configuration/cpp-general.png)
- ```Project > C++ Properties > Linker > General```
![/06_Resources/linker-general.png](/06_Resources/Visual_Studio_Project_Configuration/linker-general.png)
- ```Project > C++ Properties > Linker > Input```
![/06_Resources/linker-input.png](/06_Resources/Visual_Studio_Project_Configuration/linker-input.png)

### Start
When developing simply use the ```Local Windows Debugger``` button.

Or if trying to execute without Visual Studio navigate to
```
...\uas-ss-22-eye-tracking-video-meeting\04_Implementation\c++\x64\Debug\
```
and execute the ```C++.exe``` file.