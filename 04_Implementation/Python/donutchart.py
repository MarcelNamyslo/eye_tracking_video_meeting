import matplotlib.pyplot as plt
import csv
import os

"""
Donutchart Class, for generating the donutchart shown in the final statistic
"""


pathToEyeTrackerExe = os.path.join("..", "c++", "x64", "Debug")
input_path = os.path.join(pathToEyeTrackerExe, "csvdata.csv")


def main():
    """
    Method for aggregating all data from the csvdata.csv file to convert it into a comprehensive donutchart.
    It assigns every single gaze data to a region of a screen and counts its frequency. The size of the slots of the chart is proportional 
    to the frequency of gaze date in each region

    Returns a png with the created donutchart
    """
    self_window = 0
    others_window = 0
    upper_bar = 0
    lower_bar = 0
    leave_button = 0
    out_of_bounds = 0
    rest = 0
    sum = 0
    # Open file
    with open(input_path) as f:
        reader = csv.reader(f)
        # Iterate over rows and determine which zone is beeing looked at
        for row in reader:
            if not (row[0] == "N/A" or row[0] == "x" or row == ""):
                x = int(row[0])
                y = int(row[1])
                if (x > 1670 and x < 1910 and y > 890 and y < 1070):
                    self_window += 1
                    sum += 1
                if(x > 1670 and x < 1910 and y > 50 and y < 889):
                    others_window += 1
                    sum += 1
                if(x > 0 and x < 1775 and y > 0 and y < 35):
                    upper_bar += 1
                    sum += 1
                if(x > 0 and x < 1670 and y > 970 and y < 1070):
                    lower_bar += 1
                    sum += 1
                if(x > 1775 and x < 1900 and y > 15 and y < 35):
                    leave_button += 1
                    sum += 1
                if(x == "Person looking out of bounds!"):
                    out_of_bounds += 1
                    sum += 1
                if(x > 0 and x < 1670 and y > 35 and y < 1020):
                    rest += 1
                    sum += 1
            else:
                out_of_bounds += 1
                sum += 1
    f.close()

    size_of_groups = []
    names = []
    # Use gathered data to generate graphic
    # adds aech percentage to the chart
    if(self_window > 5):
        percentage = "{:.0%}".format(self_window/sum)
        size_of_groups.append(self_window)
        names.append("self_window" + "\n" + str(percentage))
    if(others_window > 5):
        percentage = "{:.0%}".format(others_window/sum)
        size_of_groups.append(others_window)
        names.append("others_window" + "\n" + str(percentage))
    if(upper_bar > 5):
        percentage = "{:.0%}".format(upper_bar/sum)
        size_of_groups.append(upper_bar)
        names.append("upper_bar" + "\n" + str(percentage))
    if(lower_bar > 5):
        percentage = "{:.0%}".format(lower_bar/sum)
        size_of_groups.append(lower_bar)
        names.append("lower_bar" + "\n" + str(percentage))
    if(leave_button > 5):
        percentage = "{:.0%}".format(leave_button/sum)
        size_of_groups.append(leave_button)
        names.append("leave_button" + "\n" + str(percentage))
    if(out_of_bounds > 5):
        percentage = "{:.0%}".format(out_of_bounds/sum)
        size_of_groups.append(out_of_bounds)
        names.append("out_of_screen" + "\n" + str(percentage))
    if(rest > 5):
        percentage = "{:.0%}".format(rest/sum)
        size_of_groups.append(rest)
        names.append("rest" + "\n" + str(percentage))

    plt.pie(size_of_groups,  labels=names)

    # Add a circle at the center to transform it in a donut chart
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.savefig('donutchartnew.png')


if __name__ == '__main__':
    """Application entry point"""
    main()
