from PyQt6.QtWidgets import QDialog, QWidget, QLineEdit, QTextEdit, QLabel, QPushButton, QDateEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QSizePolicy
from PyQt6.QtCore import QDate
from datetime import datetime
from src.translations import STRINGS


class AddTripDialog(QDialog):
    def __init__(self, parent=None, current_language="English"):
        super().__init__(parent)
        self.current_language = current_language
        self.setWindowTitle(STRINGS[self.current_language]["add_trip_title"])
        self.setMinimumSize(640, 480)

        layout = QVBoxLayout()

        name_label = QLabel(STRINGS[self.current_language]["name_label"])
        name_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(name_label)
        self.name_field = QLineEdit()
        self.name_field.setFocus()
        self.name_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.name_field)

        first_day_label = QLabel(STRINGS[self.current_language]["first_day_label"])
        first_day_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(first_day_label)
        self.first_day_field = QDateEdit()
        self.first_day_field.setCalendarPopup(True)
        self.first_day_field.setDate(QDate.currentDate())
        self.first_day_field.setDisplayFormat("dd.MM.yyyy")
        self.first_day_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.first_day_field)

        last_day_label = QLabel(STRINGS[self.current_language]["last_day_label"])
        last_day_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(last_day_label)
        self.last_day_field = QDateEdit()
        self.last_day_field.setCalendarPopup(True)
        self.last_day_field.setDate(QDate.currentDate())
        self.last_day_field.setDisplayFormat("dd.MM.yyyy")
        self.last_day_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.last_day_field)

        description_label = QLabel(STRINGS[self.current_language]["description_label"])
        description_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(description_label)
        self.description_field = QTextEdit()
        self.description_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.description_field)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        self.btn_add = QPushButton(STRINGS[self.current_language]["btn_add"])
        self.btn_add.clicked.connect(self.accept)
        self.btn_cancel = QPushButton(STRINGS[self.current_language]["btn_cancel"])
        self.btn_cancel.clicked.connect(self.reject)

        button_layout.addWidget(self.btn_cancel, 1)
        button_layout.addWidget(self.btn_add, 1)
        button_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(button_container)

        self.setLayout(layout)


    def accept(self):
        if not self.name_field.text().strip():
            QMessageBox.warning(self, STRINGS[self.current_language]["validation_error"], STRINGS[self.current_language]["name_required"])
            return
        if self.last_day_field.date() < self.first_day_field.date():
            QMessageBox.warning(self, STRINGS[self.current_language]["validation_error"], STRINGS[self.current_language]["last_day_before"])
            return
        try:
            datetime.strptime(self.first_day_field.text(), "%d.%m.%Y").date()
        except ValueError:
            QMessageBox.warning(self, STRINGS[self.current_language]["validation_error"], STRINGS[self.current_language]["first_day_format"])
            return
        try:
            datetime.strptime(self.last_day_field.text(), "%d.%m.%Y").date()
        except ValueError:
            QMessageBox.warning(self, STRINGS[self.current_language]["validation_error"], STRINGS[self.current_language]["last_day_format"])
            return

        super().accept()

    def get_data(self):
        return self.name_field.text(), self.first_day_field.text(), self.last_day_field.text(), self.description_field.toPlainText()