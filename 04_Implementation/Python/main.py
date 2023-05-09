from tools import readFromConfig
import graphics


"""
Main Class, handling the creation and startup of the application.
"""


def main():
    """Main method for setting up the application and running it"""
    # Find out run mode
    py_application_mode = readFromConfig("PY_APPLICATION_MODE")
    print("Running in", py_application_mode, "mode!")
    # Start application
    graphics.create_start_gui(py_application_mode)


if __name__ == '__main__':
    """Application entry point"""
    main()
