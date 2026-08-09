from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPushButton, QListWidget, QLabel, \
    QSizePolicy, QScrollArea, QListWidgetItem, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from src.views.add_trip_dialog import AddTripDialog
from src.database.trip_repository import db_add_trip, db_delete_trip, get_all_trips, get_trip_by_id
from datetime import datetime


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
        self.btn_add = QPushButton("Add")
        self.btn_add.clicked.connect(self.add_trip)
        self.btn_del = QPushButton("Delete")
        self.btn_del.clicked.connect(self.del_trip)

        button_layout.addWidget(self.btn_add, 1)
        button_layout.addWidget(self.btn_del, 1)
        button_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.trip_list = QListWidget()
        self.trip_list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.trip_list.currentItemChanged.connect(self.update_info)

        left_layout.addWidget(button_container)
        left_layout.addWidget(self.trip_list)

        self.info_widget = QLabel("Choose the trip.")
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

        self.add_all_trips()


    def add_trip(self):
        dialog = AddTripDialog(self)

        if dialog.exec():
            trip_name, trip_first_day, trip_last_day, trip_description = dialog.get_data()
            trip_id = db_add_trip(trip_name, trip_first_day, trip_last_day, trip_description)
            item = QListWidgetItem(trip_name)
            item.setData(Qt.ItemDataRole.UserRole, trip_id)
            self.trip_list.addItem(item)
            self.trip_list.setCurrentItem(item)
            self.update_info()


    def del_trip(self):
        current_item = self.trip_list.currentItem()

        if current_item is not None:
            trip_id = current_item.data(Qt.ItemDataRole.UserRole)
            db_delete_trip(trip_id)
            self.trip_list.clear()
            self.add_all_trips()
        else:
            QMessageBox.warning(self, "Warning", "No trip selected.")


    def add_all_trips(self):
        trips = get_all_trips()
        trips = sorted(trips, key=lambda x: datetime.strptime(x['first_day'], "%d.%m.%Y"))
        for trip in trips:
            item = QListWidgetItem(trip['name'])
            item.setData(Qt.ItemDataRole.UserRole, trip['id'])
            self.trip_list.addItem(item)

    def update_info(self):
        current_item = self.trip_list.currentItem()
        if current_item is not None:
            trip_id = current_item.data(Qt.ItemDataRole.UserRole)
            trip = get_trip_by_id(trip_id)
            self.info_widget.setText(f"<b>{trip['name']}</b><br>{trip['first_day']} - {trip['last_day']}<br>{trip['description']}")
        else:
            self.info_widget.setText("Choose the trip.")