# Script for converting FrameworkV1 files. A update console.
from genericpath import isfile
from gettext import find
from importlib.resources import path
from msilib.schema import File
import requests, zipfile, io, pathlib, os, shutil, stat
import config

# console colors.
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def GetNewPath(Dir):
    Dir = Dir[Dir.find("wosa_"):]
    Dir = "downloaded\\fivem-frameworkv1-master\\" + Dir

    return Dir 

def HandleFile(Dir, Filename):
    if Filename.find("_config") != -1:
        shutil.copyfile(Dir, GetNewPath(Dir))
        Log("Copied " + Filename + " to " + GetNewPath(Dir) + ".")

def UnlockDir(Dir):
    for subdir, dirs, files in os.walk(Dir):
        for file in files:
            
            os.chmod(os.path.join(subdir, file), stat.S_IWRITE)

def Start():

    # some info text
    Log("Your fellow console is now up and is soon updating your wosa frameworkv1.")
    Log("Before we start, please make sure the following...", bcolors.WARNING)
    Log("- Closed any folders or/and programs accessing the framework dir.", bcolors.WARNING)
    Log("- Stopped the FiveM server running the framework.", bcolors.WARNING)
    Log("")
    Log("")

    input(bcolors.FAIL + "Press enter when you are sure: ")

    # Cleaning up from previous executions.
    Log("Cleaning up from previous executions.")
    if os.path.isdir("downloaded\\" + config.framework_folder_name):
        shutil.rmtree("downloaded\\" + config.framework_folder_name)
        Log("Cleaned up: removed un-used folder.", bcolors.WARNING)

    if os.path.isdir("downloaded\\fivem-frameworkv1-master"):
        shutil.rmtree("downloaded\\fivem-frameworkv1-master")
        Log("Cleaned up: removed un-used folder.", bcolors.WARNING)

    if os.path.isdir("downloaded\\fivem-frameworkv1-master\\.git"):
        # Unlock .git folder.
        UnlockDir("downloaded\\fivem-frameworkv1-master\\.git")

        shutil.rmtree("downloaded\\fivem-frameworkv1-master\\.git")
        Log("Cleaned up: Removed .git folder found in local folder so a new one can be copied.", bcolors.WARNING)
    Log("")

    # Start downloading stuff.
    Log("Requesting files and preparing download.")
    r = requests.get("https://github.com/WosaFramework/fivem-frameworkv1/archive/refs/heads/master.zip", stream=True, headers={"Authorization":"token " + config.github_token})
    Log("Downloading zipped folder from github master. This may take a while, Please be patient.")
    z = zipfile.ZipFile(io.BytesIO(r.content))
    Log("Extract files to '@/downloaded/'.")
    z.extractall(r"downloaded")
    Log("")

    # Copy the required config files.
    for subdir, dirs, files in os.walk(config.framework_path + config.framework_folder_name + "\\"):
        for file in files:
            HandleFile(os.path.join(subdir, file), file)
    
    # Check for .git folder.
    if os.path.isdir(config.framework_path + config.framework_folder_name + "\\.git"):
        shutil.copytree(config.framework_path + config.framework_folder_name + "\\.git", "downloaded\\fivem-frameworkv1-master\\.git")
        Log("Copied .git folder found.", bcolors.OKBLUE)

    # Removing original files.
    Log("Removing original data before importing new...")

    # Unlock framework folder on both ends.
    UnlockDir(config.framework_path + config.framework_folder_name)
    UnlockDir("downloaded\\fivem-frameworkv1-master\\")

    shutil.rmtree(config.framework_path + config.framework_folder_name)

    # Now move the new files to the original directory.
    Log("Moving updated files back to original directory...")
    os.rename("downloaded\\fivem-frameworkv1-master", "downloaded\\" + config.framework_folder_name)
    shutil.move("downloaded\\" + config.framework_folder_name, config.framework_path)
    Log("All files moved! Your set")


def Log(str, Color = None):
    if str == "":
        print(bcolors.OKGREEN + "")
    else:

        if Color == None:
            Color = bcolors.OKGREEN
        
        print(Color + str)


# Start script :)
Start()