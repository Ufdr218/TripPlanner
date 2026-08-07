from PyQt6.QtWidgets import QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from pathlib  import Path

class MainWindow(QMainWindow):
    def __init__(self, icon_path):
        super().__init__()

        self.setWindowTitle("TripPlanner")
        self.setMinimumSize(640, 480)
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        text_label = QLabel("TripPlanner main window")
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(text_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

