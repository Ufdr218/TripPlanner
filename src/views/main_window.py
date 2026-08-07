from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPushButton, QListWidget, QLabel, QSizePolicy, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self, icon_path):
        super().__init__()

        self.setWindowTitle("TripPlanner")
        self.setMinimumSize(640, 480)
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        layout = QSplitter(Qt.Orientation.Horizontal)
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        self.add_btn = QPushButton("Добавить")
        self.del_btn = QPushButton("Удалить")
        button_layout.addWidget(self.add_btn, 1)
        button_layout.addWidget(self.del_btn, 1)
        button_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.trip_list = QListWidget()
        self.trip_list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        left_layout.addWidget(button_container)
        left_layout.addWidget(self.trip_list)

        self.info_widget = QLabel("Выберите поездку")
        self.info_widget.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.info_widget.setMargin(15)
        self.info_widget.setWordWrap(True)
        scroll_info = QScrollArea()
        scroll_info.setWidgetResizable(True)
        scroll_info.setWidget(self.info_widget)
        scroll_info.setMinimumWidth(200)

        layout.addWidget(left_container)
        layout.addWidget(scroll_info)

        layout.setSizes([320, 320])
        layout.setChildrenCollapsible(False)

        self.setCentralWidget(layout)

