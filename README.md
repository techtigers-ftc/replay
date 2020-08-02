# Introduction
This is a repository that contains all the mission program code for the **Tech Tigers** RePlay season

# Replay repo directories

The Spike Prime app does not allow multi-file projects. This means that building complex projects will result in a very long file. This makes it hard to organize, develop, and troubleshoot your code. There is also no way to share code across two Spike Prime projects. A spike prime project is stored as a binary file with a `.llsp` extension. This is actually a zip file. Git cannot interpret the binary file, and this makes it impossible to see differences in code.

To solve the problem, we take advantage of the **micropython REPL** running on the Spike Prime, and use a tool called ampy to put files directly on the spike hub.  We then can import the files in the spike app to use them.

## Directory Structure
This repository has 2 directories:
    - **spike**: contains the projects that are run in the Spike Prime app. These files end with `.llsp`
    - **lib**: contains the class and mission program files that will be loaded on to the Spike Prime hub. These files end with `.py` 


# Deploying *spike* files to the hub
Create the file on the Spike App, connect to Spike hub to the App, and run the file that needs to be deployed.
# Deploying *lib* files to the hub
## Prerequisites
Download and install ampy
Install [ampy](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy)
Type `ampy --help` in the terminal to see commands for ampy
To find the port name, type `cd /dev` in the terminal, and type `ls`
Look for a device that starts with `tty.LEGOHubLillian` and copy it
## Deployment
Create the file using your favorite editor (we recommend [Visual Studio Code](https://code.visualstudio.com/download)).

You can use ampy to copy files to the spike prime hub like this:
```sh
ampy -p /dev/ttyUSBxxxx put my_file.py
```
- where the **/dev/ttyUSBxxxx** should the device you copied, and **my_file.py** is the name of the file that needs to be deployed
