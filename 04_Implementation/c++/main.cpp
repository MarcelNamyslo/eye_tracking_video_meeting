#define NOMINMAX

#include <fstream>
#include <iostream>
#include <string>
#include <Windows.h>
#include <algorithm>
#include <fstream>
#include <sstream>
#include "interaction_lib/InteractionLib.h";
#include "interaction_lib/misc/InteractionLibPtr.h";

// Set namespace
using namespace std;

// Global variables
float screenWidth;
float screenHeight;

// Method to check the state of an option in the config file
std::string checkEyetrackerConfig(std::string optionName)
{
    // Open file
    std::ifstream configFile;
    configFile.open("config.txt");

    if (configFile.is_open())
    {
        std::string tp;
        // Iterate over all lines
        while (getline(configFile, tp))
        {
            // Ignore comment lines, check if option in line
            if (tp.find("//") == std::string::npos && tp.find(optionName) != std::string::npos)
            {
                // If option in line return it's value
                tp.replace(0, optionName.length() + 1, "");
                configFile.close();
                return tp;
            }
        }
        configFile.close();
    }
    // Else return "N/A"
    return "N/A";
}

// Method that inclusive limits a given value to the upper and lower limit
float clamp(float n, float lower, float upper)
{
    return std::max(lower, std::min(n, upper));
}

// Method to write a line into the csvdata.csv file
int doFileWrite(std::string data)
{
    std::ofstream outfile1("csvdata.csv", std::ios_base::app);
    outfile1 << std::unitbuf;
    outfile1 << data << std::endl;
    outfile1.close();
    return 0;
}

int main()
{
    // Get a handle to the desktop window
    RECT desktop;
    const HWND hDesktop = GetDesktopWindow();
    // Get the size of screen to the variable desktop
    GetWindowRect(hDesktop, &desktop);
    // The top left corner will have coordinates (0,0)
    // and the bottom right corner will have coordinates (max_screen_x, max_screen_y)
    int horizontal = desktop.right;
    int vertical = desktop.bottom;
    screenWidth = horizontal;
    screenHeight = vertical;

    std::cout << "Screen resolution: " << screenWidth << "x" << screenHeight;

    // Create and setup the interaction library
    IL::UniqueInteractionLibPtr intlib(IL::CreateInteractionLib(IL::FieldOfUse::Interactive));
    intlib->CoordinateTransformAddOrUpdateDisplayArea(screenWidth, screenHeight);
    float offset = 0.0f;
    intlib->CoordinateTransformSetOriginOffset(offset, offset);

    // Create a blank csvdata.csv file
    std::ofstream outfile;
    outfile.open("csvdata.csv");
    outfile << "x,y,validity,timestamp,id\n";
    outfile.close();

    // Subscribe to gaze point data, print data to stdout when called
    intlib->SubscribeGazePointData([](IL::GazePointData evt, void *context)
    {
        std::ofstream outfile;
        outfile.open("csvdata.csv", std::ios_base::app);

        if (evt.validity == IL::Validity::Valid)
        {
            outfile << int(clamp(evt.x, 0, screenWidth))
                << "," << int(clamp(evt.y, 0, screenHeight))
                << ",valid"
                << "," << evt.timestamp_us
                // Last value always 0 as it held the area ID that was calculated on the C++ side of the application during earlier times.
                // It is still kept here to not break any dependencies on the Python side of the application and to not risk any OutOfBounds errors etc.
                << ",0\n";
            outfile.flush();
        }
        // In case of errors or invalid eye data, print a corresponding line to file
        else
        {
            outfile << "N/A"
                << ",N/A"
                << ",invalid"
                << "," << evt.timestamp_us
                // Last value always 0 as it held the area ID that was calculated on the C++ side of the application during earlier times.
                // It is still kept here to not break any dependencies on the Python side of the application and to not risk any OutOfBounds errors etc.
                << ",0\n";
            outfile.flush();
        }
        outfile.flush();
        outfile.close();

        // Print current datapoint to the CLI
        std::cout
            << "x: " << clamp(evt.x, 0, screenWidth)
            << ", y: " << clamp(evt.y, 0, screenHeight)
            << ", validity: " << (evt.validity == IL::Validity::Valid ? "valid" : "invalid")
            << ", timestamp: " << evt.timestamp_us << " us"
            // Last value always 0 as it held the area ID that was calculated on the C++ side of the application during earlier times.
            // It is still kept here to not break any dependencies on the Python side of the application and to not risk any OutOfBounds errors etc.
            << ",0\n";
    }, nullptr);

    std::cout << "Starting interaction library update loop.\n";

    // Setup and maintain device connection, wait for device data between events and
    // Update interaction library to trigger all callbacks
    while (true)
    {
        // Check if in developer mode or not
        if (checkEyetrackerConfig("C_APPLICATION_MODE") == "DEV")
        {
            // Debug output to test application responsiveness
            if (GetKeyState('A') & 0x8000)
            {
                std::cout << "DEBUG\n";
            }
            // Debug output to collect datapoints
            if (GetKeyState('B') & 0x8000)
            {
                // If eyetracker mode is 1, collection of data is permitted
                if (checkEyetrackerConfig("EYETRACKER_MODE") == "1")
                {
                    intlib->WaitAndUpdate();
                }
                // If eyetracker mode is 0, exit application
                else if (checkEyetrackerConfig("EYETRACKER_MODE") == "0")
                {
                    break;
                }
            }
            // Quit application
            if (GetKeyState('C') & 0x8000)
            {
                break;
            }
        }
        // If not in Debug mode
        else
        {
            // Collect datapoints if confing allows (eyetracker mode is 1)
            if (checkEyetrackerConfig("EYETRACKER_MODE") == "1")
            {
                intlib->WaitAndUpdate();
            }
            // If eyetracker mode is 0, exit application
            else if (checkEyetrackerConfig("EYETRACKER_MODE") == "0")
            {
                break;
            }
        }
    }
    return 0;
}
