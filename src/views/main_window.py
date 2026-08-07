from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPushButton, QListWidget, QLabel, QSizePolicy, QScrollArea
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from src.views.add_trip_dialog import AddTripDialog


class MainWindow(QMainWindow):
    def __init__(self, icon_path):
        super().__init__()
        self.icon_path = icon_path
        self.setWindowTitle("TripPlanner")
        self.setMinimumSize(640, 480)
        if self.icon_path.exists():
            self.setWindowIcon(QIcon(str(self.icon_path)))

        layout = QSplitter(Qt.Orientation.Horizontal)
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        self.btn_add = QPushButton("Добавить")
        self.btn_add.clicked.connect(self.add_trip)
        self.btn_del = QPushButton("Удалить")
        self.btn_del.clicked.connect(self.del_trip)

        button_layout.addWidget(self.btn_add, 1)
        button_layout.addWidget(self.btn_del, 1)
        button_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.trip_list = QListWidget()
        self.trip_list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.trip_list.currentItemChanged.connect(self.update_info)

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


    def add_trip(self):
        dialog = AddTripDialog(self)

        if dialog.exec():
            trip_name, trip_first_day, trip_last_day, trip_description = dialog.get_data()
            print(trip_name)
            print(trip_first_day)
            print(trip_last_day)
            print(trip_description)
            print("________________________________")
            self.trip_list.addItem(trip_name)


    def del_trip(self):
        current_row = self.trip_list.currentRow()

        if current_row != -1:
            self.trip_list.blockSignals(True)
            removed_item = self.trip_list.takeItem(current_row)
            del removed_item

            self.trip_list.blockSignals(False)

            new_row = -1
            self.trip_list.setCurrentRow(new_row)
            self.update_info()
        else:
            print("Сначала выберите поездку для удаления!")


    def update_info(self):
        print(f'update row {self.trip_list.currentRow() + 1}')