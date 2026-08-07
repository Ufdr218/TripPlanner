import sys
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow


def create_app(icon_path):
    app = QApplication(sys.argv)
    app.setApplicationName("TripPlanner")
    window = MainWindow(icon_path)
    return app, window