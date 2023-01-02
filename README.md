# Software-engineer-assignment
+ Python project for software engineer job interview. 

### Author
+ Martin P.

### Purpose of the Package
+ Purpose of test assignment is 
to develeop a simple GUI application for connecting and gathering data from encoder device.


### Dependencies
+ serial
+ PyQt5
+ pyqtgraph

### Installation

pip install software-engineer-assignment-final

### Modules
+ main_app.py - contains main method for the application
+ gui_main.py - contains main gui class 
+ gui_components.py - contains gui component classes for used PyQt widgets
+ gui_alarm_module.py - contains class for logging encoder alarms in to the file
+ encoder_interface.py - contains interface class for encoder
+ serial_interface.py - contains basic class for serial interface

### Main Method/Usage
+ Start the application by calling App() method from main_app.py in your main.py script.

+ Example:

	from software_engineer_assignment import app

	if __name__ == '__main__':
	    app()


