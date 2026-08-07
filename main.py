import sys
from PyQt6.QtWidgets import QApplication
from src.app import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("My App")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())