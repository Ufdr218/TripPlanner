from PyQt6.QtWidgets import QDialog, QWidget, QLineEdit, QTextEdit, QLabel, QPushButton, QDateEdit, QVBoxLayout, QHBoxLayout, QMessageBox, QSizePolicy
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QKeyEvent


class AddTripDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Trip")
        self.setMinimumSize(640, 480)

        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        self.btn_add = QPushButton("Add")
        self.btn_add.clicked.connect(self.accept)
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.reject)

        button_layout.addWidget(self.btn_cancel, 1)
        button_layout.addWidget(self.btn_add, 1)
        button_container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout()

        name_label = QLabel("Name")
        name_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(name_label)
        self.name_field = QLineEdit()
        self.name_field.setFocus()
        self.name_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.name_field)

        first_day_label = QLabel("First Day")
        first_day_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(first_day_label)
        self.first_day_field = QDateEdit()
        self.first_day_field.setCalendarPopup(True)
        self.first_day_field.setDate(QDate.currentDate())
        self.first_day_field.setDisplayFormat("dd.MM.yyyy")
        self.first_day_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.first_day_field)

        last_day_label = QLabel("Last Day")
        last_day_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(last_day_label)
        self.last_day_field = QDateEdit()
        self.last_day_field.setCalendarPopup(True)
        self.last_day_field.setDate(QDate.currentDate())
        self.last_day_field.setDisplayFormat("dd.MM.yyyy")
        self.last_day_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(self.last_day_field)

        description_label = QLabel("Description")
        description_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(description_label)
        self.description_field = QTextEdit()
        self.description_field.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.description_field)
        layout.addWidget(button_container)

        self.setLayout(layout)


    def accept(self):
        if not self.name_field.text().strip():
            QMessageBox.warning(self, "Validation Error", "The 'Name' field is required.")
            return
        if self.last_day_field.date() < self.first_day_field.date():
            QMessageBox.warning(self, "Validation Error", "The last day of the trip can not be before the first day of the trip.")
            return
        super().accept()

    def get_data(self):
        return self.name_field.text(), self.first_day_field.text(), self.last_day_field.text(), self.description_field.toPlainText()