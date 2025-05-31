import sys
from PyQt6.QtWidgets import QApplication
from src.view.BinarizationApp import BinarizationApp
from src.controller.Controller import Controller

def main():
    app = QApplication(sys.argv)
    controller = Controller(None)
    window = BinarizationApp(controller)

    controller.view = window
    window.show()
    sys.exit(app.exec())  

if __name__ == "__main__":
    main()
