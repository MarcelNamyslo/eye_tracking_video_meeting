import os
import time
import csv
import pandas as pd
from tkinter import *
from tkinter.ttk import Style
from tkinter.ttk import Notebook
from tkinter.constants import DISABLED, NORMAL
from PIL import Image, ImageTk
from matplotlib.figure import Figure
import graphics
from graphicsCalculations import linegraph_creator
from tools import writeToConfig, readFromConfig


"""
Processing Class, taking care of all processing steps to interpret incoming data

IMPORTANT:
- This application assumes the user is using a Full HD monitor (1920x1080)
"""


# +-----------------------------------------------------------------+
# |                                                                 |
# |   START OF PROCESSING METHODS - GRAPHICAL METHODS AT LINE 240   |
# |                                                                 |
# +-----------------------------------------------------------------+


pathToEyeTrackerExe = os.path.join("..", "c++", "x64", "Debug")
input_path = os.path.join(pathToEyeTrackerExe, "csvdata.csv")
# Wait times in seconds after a popup and initially pressing the start button
wait_after_popup = 1
wait_before_startup = 3

# Zones schema: name, top left corner x&y, bottom right corner x&y
zones = [
    ["self_window", [1670, 890], [1910, 1070]],
    ["others_window", [1670, 50], [1910, 889]],
    ["upper_bar", [0, 0], [1775, 35]],
    ["lower_bar", [10, 970], [1670, 1070]],
    ["leave_button", [1775, 15], [1900, 35]],
    ["out_of_bounds", [], []]
]
# Schema: name, focusDatapointsNeeded, repeatedFocusDatapoints
zone_config = [
    ["self_window", 120, 0],
    ["others_window", 120, 0],
    ["upper_bar", 120, 0],
    ["lower_bar", 120, 0],
    ["leave_button", 120, 0],
    ["out_of_bounds", 120, 0]
]
# Schema: eventname, (array) list holding a unix timestamp + CSV line when the event was triggered + focusDatapointsNeeded + boolean if detection was correct
zone_stats = [
    ["self_window", []],
    ["others_window", []],
    ["upper_bar", []],
    ["lower_bar", []],
    ["leave_button", []],
    ["out_of_bounds", []]
]
# Schema: (array) list holding eventname + unix timestamp + CSV line when the event was triggered + focusDatapointsNeeded + boolean if detection was correct
zone_events = []


def main():
    """
    Main eventloop doing all the processing and generating popups

    Whole class will be concipated around beeing run as a subprocess and never interacted with.
    This way we can synchronously start/stop this class with the eyetracker if they both read from the config.
    """
    # Startup delay
    for i in range(wait_before_startup, 0, -1):
        print("Starting in", i, "seconds...")
        time.sleep(1)
    # Write into config that recording can start
    writeToConfig("EYETRACKER_MODE", "1")
    # Variable that holds the last processed line in the CSV file until the process is killed
    lastProcessedDatapoint = 1

    # Main class loop
    while True:
        # Don't process data until mode is reset
        if readFromConfig("EYETRACKER_MODE") == "2":
            print("Processing paused...")
            time.sleep(0.1)
            continue
        # Print stats and exit
        if readFromConfig("EYETRACKER_MODE") == "0":
            create_summary()
            break
        # Iterate over csvdata.csv skipping lines 1 ... lastProcessedDatapoint to not reprocess data
        for chunk in pd.read_csv(os.path.join(pathToEyeTrackerExe, "csvdata.csv"), skiprows=[i for i in range(1, lastProcessedDatapoint)], chunksize=1):
            # Check for changes in config and break out of for loop
            if readFromConfig("EYETRACKER_MODE") == "2" or readFromConfig("EYETRACKER_MODE") == "0":
                break

            # Increment as new line was found and is beeing processed
            lastProcessedDatapoint += 1

            # Iterate over all zones
            for zone in zones:
                try:
                    # Check if looking out of bounds
                    if str(chunk.iloc[0]["x"]) == "nan":
                        # Add 1 iteration to zone for enduring focus and eval if popup is needed (threshold reached)
                        evalZoneFocus("out_of_bounds", lastProcessedDatapoint)
                        # RESET ALL OTHER ZONES
                        for zone_1 in zones:
                            if zone_1[0] != "out_of_bounds":
                                writeZoneConfig(zone_1[0], 2, 0)
                        break
                    else:
                        # Skip this one as there are now coordinates
                        if zone[0] == "out_of_bounds":
                            writeZoneConfig(zone[0], 2, 0)
                            continue
                        # Check if current datpoint is in curent zones x
                        if int(zone[1][0]) <= int(chunk.iloc[0]["x"]) <= int(zone[2][0]):
                            # Check if current datpoint is in curent zones y
                            if int(zone[1][1]) <= int(chunk.iloc[0]["y"]) <= int(zone[2][1]):
                                # Add 1 iteration to zone for enduring focus and eval if popup is needed (threshold reached)
                                evalZoneFocus(zone[0], lastProcessedDatapoint)
                                continue
                    writeZoneConfig(zone[0], 2, 0)
                except IndexError:
                    # print(str(chunk.iloc[0]["x"]))
                    # print(traceback.format_exc())
                    print("IndexError: probably no new data!")
                    time.sleep(0.1)


def writeZoneConfig(zone_name: str, stat_arr_pos: int, new_value: int):
    """
    Method to write a new value to a position in the zone_config array of a specific zone

    Parameters
    ----------
    zone_name: str
        Name of the zone.
    stat_arr_pos: int
        Array position of the value to edit.
    new_value: int
        The new value to be written.
    """
    for zone in zone_config:
        if zone[0] == zone_name:
            zone[stat_arr_pos] = new_value
            break


def readZoneConfig(zone_name: str, stat_arr_pos: int):
    """
    Method to read from a specific zone in zone_config

    Parameters
    ----------
    zone_name: str
        Name of the zone.
    stat_arr_pos: int
        Array position of the value to read.
    """
    for zone in zone_config:
        if zone[0] == zone_name:
            return zone[stat_arr_pos]


def addZoneStatistic(zone_name: str, csvLine: int, focusDatapointsNeeded: int, accepted: bool):
    """
    Method to add a timestamp with event to the zone and the global queue

    Parameters
    ----------
    zone_name: str
        Name of the zone.
    csvLine: int
        Line number in the csvdata.csv file where the datapoint in question is located.
    focusDatapointsNeeded: int
        How many datapoints in a row have to be of this event type to trigger a popup.
    accepted: bool
        If detection of event was correct or false positive.
    """
    with open(os.path.join(pathToEyeTrackerExe, "csvdata.csv")) as f:
        reader = csv.reader(f)
        raw = list(reader)

    for zone in zone_stats:
        if zone[0] == zone_name:
            # Add event to global event list for later processing
            zone[1].append([raw[csvLine][3], csvLine,
                           focusDatapointsNeeded, accepted])
            zone_events.append([zone[0], int(raw[csvLine][3]), csvLine -
                               readZoneConfig(zone[0], 1), readZoneConfig(zone[0], 1), accepted])
            break


def evalZoneFocus(zone: str, lastProcessedDatapoint: int):
    """
    Method that increments the repeatedFocusDatapoints counter and checks if focusDatapointsNeeded is needed to spawn a popup

    Parameters
    ----------
    zone: str
        Name of the zone.
    lastProcessedDatapoint: int
        Line number in the csvdata.csv file where the datapoint in question is located.
    """
    # If so increment variable in zone_config that keeps track how long focus has been maintained
    writeZoneConfig(zone, 2, readZoneConfig(zone, 2) + 1)
    # If threshhold is reached react accordingly
    if readZoneConfig(zone, 2) >= readZoneConfig(zone, 1):
        writeToConfig("EYETRACKER_MODE", "2")
        print("Focused on zone", zone, "for over", readZoneConfig(zone, 1) / 60,
              "second(s) at", lastProcessedDatapoint, "minus", readZoneConfig(zone, 1))
        correctDetection = True
        if zone == "self_window":
            correctDetection = create_solo_popup(1)
        elif zone == "others_window":
            correctDetection = create_solo_popup(2)
        elif zone == "upper_bar":
            correctDetection = create_solo_popup(3)
        elif zone == "lower_bar":
            correctDetection = create_solo_popup(4)
        elif zone == "leave_button":
            correctDetection = create_solo_popup(5)
        elif zone == "out_of_bounds":
            correctDetection = create_solo_popup(6)

        addZoneStatistic(zone, lastProcessedDatapoint - readZoneConfig(zone,
                         1), readZoneConfig(zone, 1), correctDetection)
        # RESET ALL ZONES
        for zone_1 in zones:
            writeZoneConfig(zone_1[0], 2, 0)


# +------------------------------------------------------------------+
# |                                                                  |
# |   END OF PROCESSING METHODS - ONLY GRAPHICAL METHODS FOLLOWING   |
# |                                                                  |
# +------------------------------------------------------------------+


# Fonts for Gui
FONT_FOR_TEXT_BOLD = ("Arial", 13, "bold")
FONT_FOR_TEXT = ('Arial', 13)
FONT_FOR_HEADLINE = ('Arial', 18)

# Background and button color
bg_color = '#98D4BB'
button_color = '#218B82'

# Indicates whether the attention loss popup has been correct or wrong. Somehow needs to be global?
popup_acceptance = False
# Indicates whether there data is being recorded. Needs to be global as multiple functions need this info.
recording = None
proc = None
my_proc = None

# Keeps references to the Gui window and a button, to keep access throughout the run of this program.
win = None


def create_solo_popup(reason: int):
    """
    Creates a popup to get the users attention about an event that occured

    Attributes
    ----------
    reason: int
        Why the popup should be generated/What the user did to trigger this event.
    """
    # create popup window
    pop_win = Tk()
    pop_win.geometry('500x300')
    pop_win.resizable(False, False)
    pop_win.title('An event occured')
    pop_win.configure(bg=bg_color)

    global win
    win = pop_win

    def on_reject_popup():
        """
        Indicates that the attention popup has been rejected
        """
        global popup_acceptance, my_proc, proc
        print("The Recording of attention continues.")
        # save user feedback about correctness of attention loss detection
        popup_acceptance = False
        # close popup window
        pop_win.destroy()
        # wait before resuming the recording
        for i in range(wait_after_popup, 0, -1):
            print("Resuming in", i, "seconds...")
            time.sleep(1)
        # starts the eyetracker again
        writeToConfig("EYETRACKER_MODE", "1")

    def on_accept_popup():
        """
        Indicates that the attention popup has been accepted, function to be called when popup is  accepted
        """
        global popup_acceptance, my_proc, proc
        print("The Recording of attention continues.")
        # save user feedback about correctness of attention loss detection
        popup_acceptance = True
        # close popup window
        pop_win.destroy()
        # wait before resuming the recording
        for i in range(wait_after_popup, 0, -1):
            print("Resuming in", i, "seconds...")
            time.sleep(1)
        # starts the eyetracker again
        writeToConfig("EYETRACKER_MODE", "1")

    # Create buttons for accepting and rejecting the popup
    reject_button = Button(pop_win, text='I was paying attention!', width=20, height=1, bg=button_color,
                           font=FONT_FOR_TEXT_BOLD, command=on_reject_popup)
    reject_button.place(x=180, y=240)
    accept_button = Button(pop_win, text='OK', width=5, height=1, bg=button_color, font=FONT_FOR_TEXT_BOLD,
                           command=on_accept_popup)
    accept_button.place(x=410, y=240)

    # Creating labels
    text1 = Label(pop_win, text='Hey there! It seems like you have lost \nfocus.', font=FONT_FOR_TEXT_BOLD,
                  bg=bg_color, justify='left')
    text1.place(x=130, y=50)

    # Different text for different causes of attention loss
    if reason == 1:
        text_for_label = 'You have been looking at yourself for a \nprolonged time.'
    elif reason == 2:
        text_for_label = 'You have been looking at the other \nparticipants for a prolonged time.'
    elif reason == 3:
        text_for_label = 'You have been looking at the upper \nbar for a \nprolonged time..'
    elif reason == 4:
        text_for_label = 'You have been looking at the lower \nbar for a \nprolonged time..'
    elif reason == 5:
        text_for_label = 'You have been looking at the leave \nbutton for a \nprolonged time..'
    else:
        text_for_label = 'You have looked out of the window for a prolonged time'

    text2 = Label(pop_win, text=text_for_label,
                  font=FONT_FOR_TEXT, bg=bg_color, justify='left')
    text2.place(x=20, y=140)

    # Import the lightbulb picture and resize it to fit properly
    wd = os.getcwd()
    photoimage = ImageTk.PhotoImage(
        Image.open(os.path.join("resources", "lightbulb.png")).resize((90, 90)))
    os.chdir(wd)
    width, height = photoimage.width(), photoimage.height()

    # Put the lightbulb image in a label
    label = Label(pop_win, image=photoimage, width=width,
                  height=height, bg=bg_color)
    label.image = photoimage
    label.place(x=20, y=30)

    pop_win.mainloop()

    return popup_acceptance


def create_some_data():
    """
    Creates the attention graph and makes it visually appealing
    """
    with open(input_path) as f:
        reader = csv.reader(f)
        raw = list(reader)

    #this section detects the correct start and endtime from csv list
    #since there could be different variation of each row (showing x and y or out of bounds) in the list
    #we had to filter for the correct timestamp
    starttime = 0
    endtime = 0

    if len(raw[1]) == 5:
        starttime = raw[1][3]
    elif len(raw[1]) == 2:
        starttime = raw[1][1]

    if len(raw[-1]) == 5:
        endtime = raw[-1][3]
    elif len(raw[-1]) == 2:
        endtime = raw[-1][1]
    elif len(raw[-2]) == 5:
        endtime = raw[-2][3]
    elif len(raw[-2]) == 2:
        endtime = raw[-2][1]

    #creates the fig which will be plotted
    fig = Figure(figsize=(7, 3), dpi=100)

    #list of attention score for each minute
    y_values   = linegraph_creator(starttime, endtime, zone_events)

    #claculates total score by taking the mean of every score per minute
    total_calculated_score = 0
    sum = 0
    for value in y_values:
        sum += value
    total_calculated_score = sum / len(y_values)

    #creates x axis
    x_values = [i + 0.5 for i in range(len(y_values))]
    x_values.insert(0, 0)
    x_values.append(len(y_values))
    y_values.append(y_values[len(y_values)-1])
    y_values.insert(0, 100)

    # Adding the subplot
    plot1 = fig.add_subplot(111)

    # Plotting the graph
    plot1.plot(x_values, y_values, marker='o')
    plot1.set_ylim([0, 105])
    plot1.set_xlim([0, len(y_values)-2])
    return fig, total_calculated_score


def create_summary():
    """
    Creates the starting GUI, with the start and stop buttons the eyetracking can be controlled
    """
    # create summary window
    sum_win = Tk()
    sum_win.geometry('1000x600')
    sum_win.resizable(False, False)
    sum_win.title('Summary')
    sum_win.configure(bg=bg_color)

    # create a custom style that fits our gui-mockups
    style = Style()
    style.theme_use('default')
    style.configure('TNotebook.Tab', font=FONT_FOR_TEXT, bg="green")
    style.map("TNotebook", background=[("selected", button_color)])

    style.theme_create("yummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": bg_color},
            "map": {"background": [("selected", button_color)],
                    "expand": [("selected", [1, 1, 1, 0])]}}})

    # create and add the different tabs to the summary window
    tab_control = Notebook(sum_win)

    tab1 = Frame(tab_control, bg=bg_color)
    tab2 = Frame(tab_control, bg=bg_color)
    tab3 = Frame(tab_control, bg=bg_color)
    tab4 = Frame(tab_control, bg=bg_color)

    tab_control.add(tab1, text='Summary')
    tab_control.add(tab2, text='Specific Events')
    tab_control.add(tab3, text='Heatmap')
    tab_control.add(tab4, text='DonutChart')
    tab_control.pack(expand=1, fill="both")

    # counts the number of attention losses without categorizing after reason
    detectedattentionloss = 0
    # counts the number of attention losses while categorizing after reason
    stats_count = [0, 0, 0, 0, 0, 0]
    numb = 0
    for zone in zone_stats:
        for stat in zone[1]:
            stats_count[numb] += 1
            detectedattentionloss += 1
        numb += 1

    # calls the method that creates the attention graph
    chart, totalcalculatedscore = create_some_data()

    # create the different tabs and fill them with information
    graphics.create_summary_tab_one(
        tab1, totalcalculatedscore, detectedattentionloss, chart)
    graphics.create_summary_tab_two(tab2, stats_count)
    graphics.create_summary_tab_three(tab3)
    graphics.create_summary_tab_four(tab4)
    sum_win.mainloop()


if __name__ == '__main__':
    """Application entry point"""
    main()
