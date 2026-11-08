import sys
from PyQt6.QtWidgets import QApplication
from src.views.main_window import MainWindow
from src.database.db import init_db


def create_app(icon_path, settings_icon_path, style_path):
    init_db()
    app = QApplication(sys.argv)
    app.setStyleSheet(style_path.read_text(encoding="utf-8"))
    app.setApplicationName("TripPlanner")
    window = MainWindow(icon_path, settings_icon_path)
    return app, window