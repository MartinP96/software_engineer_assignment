"""
    File name: __main__py
    Date: 02.01.2023
"""

import sys
from PyQt5 import QtWidgets
from software_engineer_assignment.gui_main import UiMainWindow


def app():
    """
    Main method for starting the app
    args: /
    return: /
    """
    gui_app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = UiMainWindow(main_window)
    main_window.show()
    sys.exit(gui_app.exec_())


if __name__ == '__main__':
    app()
