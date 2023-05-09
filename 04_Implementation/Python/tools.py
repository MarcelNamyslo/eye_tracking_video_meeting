import os


"""
Tools class, hosting any functionality needed application wide
"""


pathToEyeTrackerExe = os.path.join("..", "c++", "x64", "Debug")


def writeToConfig(configOption: str, value: str) -> None:
    """Method to write a new value to a config option

    Parameters
    ----------
    configOption : str
        The option which should be targeted.
    value : str
        The new value which should be written to the target option.

    Returns
    -------
    Nothing (None)
    """
    # Open file
    file = open(os.path.join(pathToEyeTrackerExe, "config.txt"), "r")
    replacement = ""
    # Iterate over every line
    for line in file:
        line = line.strip()
        fullConfigOption = configOption + "="
        # If option was found replace whole line with the option and new value
        if fullConfigOption in line:
            replacement = replacement + fullConfigOption + value + "\n"
        # Else just keep line
        else:
            replacement = replacement + line + "\n"
    file.close()
    # Overwrite file with newly created file content
    fout = open(os.path.join(pathToEyeTrackerExe, "config.txt"), "w")
    fout.write(replacement)
    fout.close()


def readFromConfig(configOption: str) -> str:
    """Method to read a value from a config option

    Parameters
    ----------
    configOption : str
        The option which should be targeted.

    Returns
    -------
    "N/A" if no option found or the value found (str)
    """
    # Open file
    file = open(os.path.join(pathToEyeTrackerExe, "config.txt"), "r")
    returnValue = "N/A"
    # Iterate over every line
    for line in file:
        line = line.strip()
        fullConfigOption = configOption + "="
        # If line found, save value
        if fullConfigOption in line:
            returnValue = line.replace(fullConfigOption, "")
    file.close()
    # Return value
    return returnValue
