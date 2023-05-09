import os
import subprocess
import os
import processing
import heatmap
import csv
from tkinter import *
from tkinter.ttk import Notebook
from tkinter.ttk import Style
from tkinter.constants import DISABLED, NORMAL
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from tools import writeToConfig


"""
Graphics class, handling most of the displayed graphics elements
"""

# Fonts for GUI
FONT_FOR_TEXT_BOLD = ("Arial", 13, "bold")
FONT_FOR_TEXT = ('Arial', 13)
FONT_FOR_HEADLINE = ('Arial', 18)

# Background and button color
bg_color = '#98D4BB'
button_color = '#218B82'

# Indicates whether the attention loss popup has been correct or wrong
popup_acceptance = False
# Indicates whether there data is being recorded
recording = None
proc = None
my_proc = None

# Keeps references to the GUI window
win = None

pathToEyeTrackerExe = os.path.join("..", "c++", "x64", "Debug")


def create_summary_tab_one(tab1, totalcalculatedscore, detectedattentionlosses, fig):
    """
    Creates the first tab, adds a few labels/figures/plots

    Parameters
    ----------
    tab1: Frame
        Frame holding data and layout of the tab.
    totalcalculatedscore: int
        variable for the total scroe calculated from the attention graph
    detectedattentionlosses: int
        total number of attention losses whatever the reason
    fig: matplotlibfigure
        graph showing the attention over time
    """
    # Add labels showing data and placing them on the window
    label_summary = Label(
        tab1, text=f'Your Summary of the last Meeting:', font=FONT_FOR_HEADLINE, bg=bg_color)
    label_summary.place(x=20, y=50)

    label_total_score = Label(
        tab1, text=f'Total calculated Score: {totalcalculatedscore}', font=FONT_FOR_TEXT_BOLD, bg=bg_color)
    label_total_score.place(x=20, y=100)

    label_no_attention_loss = Label(tab1, text=f'Detected Attention Losses: {detectedattentionlosses}', font=FONT_FOR_TEXT_BOLD,
                                    bg=bg_color)
    label_no_attention_loss.place(x=20, y=140)

    label_timeline = Label(tab1, text=f'Timeline:',
                           font=FONT_FOR_TEXT, bg=bg_color)
    label_timeline.place(x=20, y=200)

    # Add attention graph to the window
    figure = fig
    canvas_timeline = FigureCanvasTkAgg(figure, master=tab1)
    canvas_timeline.draw()
    canvas_timeline.get_tk_widget().place(x=20, y=240)


def create_summary_tab_two(tab2, data):
    """
    Creates the second tab, adds a few labels/figures/plots

    Parameters
    ----------
    tab2: Frame
        Frame holding data and layout of the tab.
    data: 1d-Array
        array holding the amount of attention losses seperated for each reason.
    """
    # Add necessary Labels to show the data
    label_summary = Label(tab2, text=f'Number of detected attention losses by Event:', font=FONT_FOR_HEADLINE,
                          bg=bg_color)
    label_summary.place(x=20, y=50)

    label_self_looks_long = Label(tab2, text=f'You have been looking at yourself {data[0]} times',
                                  font=FONT_FOR_TEXT_BOLD, bg=bg_color)
    label_self_looks_long.place(x=20, y=100)

    label_participants = Label(tab2, text=f'You have been looking at the other participants {data[1]} times', font=FONT_FOR_TEXT_BOLD,
                               bg=bg_color)
    label_participants.place(x=20, y=140)

    label_upper_bar = Label(
        tab2, text=f'You have been looking at the upper bar {data[2]} times', font=FONT_FOR_TEXT_BOLD, bg=bg_color)
    label_upper_bar.place(x=20, y=180)

    label_lowertaskbar = Label(tab2, text=f'You have been looking at the lower bar {data[3]} times',
                               font=FONT_FOR_TEXT_BOLD, bg=bg_color)
    label_lowertaskbar.place(x=20, y=220)

    label_leavebutton = Label(tab2, text=f'You have been looking at the leave button {data[4]} times',
                              font=FONT_FOR_TEXT_BOLD, bg=bg_color)
    label_leavebutton.place(x=20, y=260)

    label_outofwindow = Label(tab2, text=f'You have been looking out of window {data[5]} times',
                              font=FONT_FOR_TEXT_BOLD, bg=bg_color)
    label_outofwindow.place(x=20, y=300)


def create_summary_tab_three(tab3):
    """
    Creates the third tab, adds a few labels/figures/plots

    Parameters
    ----------
    tab3: Frame
        Frame holding data and layout of the tab.
    """
    input_path = "..\\c++\\x64\\Debug\\csvdata.csv"
    gaze_data = []
    # draws the heatmap by using the data collected in the csv file
    with open(input_path) as f:
        reader = csv.reader(f)
        for row in reader:
            if not (row[0] == "N/A" or row[0] == "x" or row == ""):
                gaze_data.append((float(row[0]), float(row[1]), 1))
    heatmap.draw_heatmap(gaze_data, (1920, 1080),  savefilename="output")
    # the heatmap is opened from a file saved in the line above
    img = Image.open("output.png")
    # resize image
    image = img.resize((900, 500))
    # add image to the window
    resultimage = ImageTk.PhotoImage(image, master=tab3)
    label = Label(tab3, image=resultimage)
    label.photo = resultimage
    label.place(x=40, y=50)


def create_summary_tab_four(tab4):
    """
    Creates the fourth tab, adds a few labels/figures/plots

    Parameters
    ----------
    tab4: Frame
        Frame holding data and layout of the tab.
    """
    global my_proc2
    # creates the donutchart and saving it by launching a subprocess that accesses the csvfile
    my_proc2 = subprocess.Popen("python donutchart.py", shell=True)
    my_proc2.wait()
    # the donutchart is opened from a png file generated and saved in the subprocess started above
    img = Image.open("donutchartnew.png")
    # resize image
    image = img.resize((640, 480))
    # add image to the window
    resultimage = ImageTk.PhotoImage(image, master=tab4)
    label = Label(tab4, image=resultimage)
    label.photo = resultimage

    label.place(x=130, y=30)


def create_start_gui(py_application_mode: str):
    """
    Creates the starting GUI, with start and stop buttons to control the eyetracking

    Parameters
    ----------
    py_application_mode: str
        The mode in which the Python application was launched
    """
    # Create window
    start_win = Tk()
    start_win.geometry('500x300')
    start_win.resizable(False, False)
    start_win.title('HelpMeFocus - Start')
    start_win.configure(bg=bg_color)

    global win
    win = start_win

    text_intro = 'Hey! \nthis is our app to help you focus longer during \nVideo Meetings with Microsoft Teams.' \
                 '\n\nTo Start the attention loss detection just press the START Button. \nTo Stop it, press the ' \
                 'STOP Button.'

    label_timeline = Label(start_win, text=text_intro,
                           font=FONT_FOR_TEXT, bg=bg_color, justify='left')
    label_timeline.place(x=20, y=20)

    # Method to be executed when the start/pause button has been pressed
    def on_start_stop():
        global recording
        global proc
        global my_proc
        # Depending on which internal mode currently is active launch different parts of the application, pause or exit it
        if recording is None or recording is False:
            print("The Recording of attention loss has started.")
            # add a "finish recording" button
            exit_button.place(x=250, y=190)

            if proc is None and my_proc is None:
                # start the eyetracker and open the corresponding subprocess to gather data
                writeToConfig("EYETRACKER_MODE", "2")
                my_proc = subprocess.Popen("python processing.py", shell=True)
                if py_application_mode == "NORMAL":
                    wd = os.getcwd()
                    proc = subprocess.Popen(
                        "start /wait C++.exe", shell=True, cwd=pathToEyeTrackerExe)
                    os.chdir(wd)
            recording = True
        # destroy the start button as the meeting is already beeing recorded
        start_stop_button.destroy()

    def finish_recording():
        """
        Method to be executed when the finish button is pressed. Ends the eyetracking and opens the summary window
        """
        global proc
        global recording
        global my_proc
        # Depending on which internal mode currently is active do nothing or exit the application
        if proc is not None or my_proc is not None:
            print("The Recording of attention loss has stopped.")
            # stop eyetracking
            writeToConfig("EYETRACKER_MODE", "0")
            proc = None
            my_proc = None
            # destroy finish button
            exit_button.destroy()
        else:
            print("Eyetracker not started yet!")

    start_stop_button = Button(start_win, text='START', width=20, height=1, bg=button_color, font=FONT_FOR_TEXT_BOLD,
                               command=on_start_stop)
    start_stop_button.place(x=50, y=190)

    exit_button = Button(start_win, text='FINISH', width=20, height=1, bg=button_color, font=FONT_FOR_TEXT_BOLD,
                         command=finish_recording)

    win.mainloop()
