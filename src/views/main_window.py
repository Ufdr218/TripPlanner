from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QPushButton, QListWidget, QLabel, \
    QSizePolicy, QScrollArea, QListWidgetItem, QMessageBox
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QIcon
from src.views.add_trip_dialog import AddTripDialog
from src.views.settings_dialog import SettingsDialog
from src.database.trip_repository import db_add_trip, db_delete_trip, get_all_trips, get_trip_by_id
from datetime import datetime
from src.translations import STRINGS


class MainWindow(QMainWindow):
    def __init__(self, icon_path, settings_icon_path):
        super().__init__()
        settings = QSettings("TripPlanner", "Settings")
        self.current_language = settings.value("Language", "English")
        self.icon_path = icon_path
        self.settings_icon_path = settings_icon_path
        self.setWindowTitle(STRINGS[self.current_language]["app_title"])
        self.setMinimumSize(640, 480)
        if self.icon_path.exists():
            self.setWindowIcon(QIcon(str(self.icon_path)))

        layout = QSplitter(Qt.Orientation.Horizontal)
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        self.btn_settings = QPushButton(STRINGS[self.current_language]["btn_settings"])
        if self.settings_icon_path.exists():
            self.btn_settings.setIcon(QIcon(str(self.settings_icon_path)))
        self.btn_settings.clicked.connect(self.open_settings)
        self.btn_add = QPushButton(STRINGS[self.current_language]["btn_add"])
        self.btn_add.clicked.connect(self.add_trip)
        self.btn_del = QPushButton(STRINGS[self.current_language]["btn_del"])
        self.btn_del.clicked.connect(self.del_trip)

        button_layout.addWidget(self.btn_settings, 1)
        button_layout.addWidget(self.btn_add, 1)
        button_layout.addWidget(self.btn_del, 1)
        button_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.trip_list = QListWidget()
        self.trip_list.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.trip_list.currentItemChanged.connect(self.update_info)

        left_layout.addWidget(button_container)
        left_layout.addWidget(self.trip_list)

        self.info_widget = QLabel(STRINGS[self.current_language]["info_widget_default"])
        self.info_widget.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.info_widget.setMargin(15)
        self.info_widget.setWordWrap(True)
        self.info_widget.setTextFormat(Qt.TextFormat.RichText)
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
        dialog = AddTripDialog(self, self.current_language)

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
            QMessageBox.warning(self, STRINGS[self.current_language]["warning"], STRINGS[self.current_language]["del_no_trip"])


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
            description = trip['description'].replace('\n', '<br>') if trip['description'] else ''
            self.info_widget.setText(f"<b>{trip['name']}</b><br>{trip['first_day']} - {trip['last_day']}<br>{description}")
        else:
            self.info_widget.setText(STRINGS[self.current_language]["info_widget_default"])

    def open_settings(self):
        dialog = SettingsDialog(self, self.current_language)
        if dialog.exec():
            language = dialog.get_data()
            settings = QSettings("TripPlanner", "Settings")
            settings.setValue("Language", language)
            self.current_language = language
            self.update_ui_language()

    def update_ui_language(self):
        self.setWindowTitle(STRINGS[self.current_language]["app_title"])
        self.btn_settings.setText(STRINGS[self.current_language]["btn_settings"])
        self.btn_add.setText(STRINGS[self.current_language]["btn_add"])
        self.btn_del.setText(STRINGS[self.current_language]["btn_del"])
        self.update_info()

