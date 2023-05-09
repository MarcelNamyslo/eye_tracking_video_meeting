# 04 Implementation

## Requirements
### Visual Studio 2022 Community Edition and Visual Studio Code
For editing C++ code, go to https://visualstudio.microsoft.com/downloads/ to download and install the VS 2022 Community Edition.

For editing Python code, also download Visual Studio Code from the same website.

### uas-ss-22-eye-tracking-video-meeting GitHub repository
Go to https://git.scc.kit.edu/issd/students/seminars/uas-ss-22-eye-tracking-video-meeting and download (Clone) the repository as you wish, or just navigate your terminal to where you want the repository to be on your machine and execute the following command (may require you to save your SSH key in your GitHub account)
```
git clone git@git.scc.kit.edu:issd/students/seminars/uas-ss-22-eye-tracking-video-meeting.git
```
When downloading don't forget to choose the right branch.

### Tobii Interaction Library SDK
The Tobii Libraries are located in:
```
...\uas-ss-22-eye-tracking-video-meeting\04_Implementation\c++\TobiiLibraries
```


## === Deprecated ===
This part is deprecated and no longer used or implemented.
### NPM and Node.js
If you still want to see our progress we did in this area go to the "Archive" folder in 04_Implementation.

To run the Zoom Web SDK example app from 
```
...\uas-ss-22-eye-tracking-video-meeting\04_Implementation\Node
```
you need to install Node and NPM for Windows (https://phoenixnap.com/kb/install-node-js-npm-on-windows).

Afther the installation navigate to the folder fitting your use case (CDN, Component or Local) and execute the following command:
```
npm install
```
When the installation process is done you can start the web app with:
```
npm start
```

### C++ Extensions for VsCode
You have to install the c++ extentions in the vscode marketplace.

### C++ part of Tobii Interaction Library SDK
We build the C++ code located in the "C++" folder by using the Visual Studio 2022 toolset.

Using the **x64 Native Tools Command Prompt for VS 2022** (just type this in your windows search box), we get the following output when running the compiler without any arguments:
```
C:\src>cl.exe
Microsoft (R) C/C++ Optimizing Compiler Version 19.16.27027.1 for x64
Copyright (C) Microsoft Corporation.  All rights reserved.
usage: cl [ option... ] filename... [ /link linkoption... ]
```
To build a C++ file the following command is needed:

```
cl.exe /EHsc /MD /I include <filename>.cpp /link /libpath:library\lib\x64 tobii_interaction_lib.lib tobii_stream_engine.lib
```
or 
```
cl.exe /EHsc /MD /I include <filename>.cpp /link  tobii_interaction_lib.lib tobii_stream_engine.lib  
```
If the buildporcess was successfull, an .exe file was generated and can be executed to test out the application.

### Zoom SDK Keys
You have to generate public and private Key for the zoom SDK (https://marketplace.zoom.us/docs/sdk/native-sdks/web/build/#option-2-import-through-cdn)

When you generated your public and private SDK Keys, you have to put them into the index.js file at line 20 and 26.

```
...\uas-ss-22-eye-tracking-video-meeting\04_Implementation\Python\static\index.js
```
Example: 
```
var SDK_KEY = "YOUR_SDK_KEY"
var SDK_SECRET = "YOUR_SDK_SECRET"
```

### Zoom Account
You need a registrated zoom account to generate keys for the zoom SDK