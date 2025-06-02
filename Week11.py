import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox,
    QDockWidget, QStatusBar, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard


class CRUDApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Week 11 - CRUD Enhancement")
        self.setGeometry(100, 100, 800, 600)

        self.data = []
        self.current_row = -1

        self.initUI()

    def initUI(self):
        # Status Bar
        status_bar = QStatusBar()
        status_bar.showMessage("Nama: Zidan Shoni Ikram | NIM: F1Do22165")
        self.setStatusBar(status_bar)

        # Central widget with scroll area
        central_widget = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)

        # Form
        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.city_input = QLineEdit()

        # Paste from clipboard
        paste_btn = QPushButton("Paste from Clipboard (to Name)")
        paste_btn.clicked.connect(self.paste_clipboard)

        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(paste_btn)
        form_layout.addWidget(QLabel("Age:"))
        form_layout.addWidget(self.age_input)
        form_layout.addWidget(QLabel("City:"))
        form_layout.addWidget(self.city_input)

        # Buttons
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_data)

        update_btn = QPushButton("Update")
        update_btn.clicked.connect(self.update_data)

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_data)

        form_layout.addWidget(add_btn)
        form_layout.addWidget(update_btn)
        form_layout.addWidget(delete_btn)

        scroll_layout.addLayout(form_layout)
        scroll_area.setWidget(scroll_container)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Age", "City"])
        self.table.cellClicked.connect(self.load_row_data)

        scroll_layout.addWidget(self.table)

        # Set scroll area as central widget
        layout = QVBoxLayout(central_widget)
        layout.addWidget(scroll_area)
        central_widget.setLayout(layout)
        self.setCentralWidget(scroll_area)

        # Dock Widget for Search
        dock = QDockWidget("Search Panel", self)
        dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea)

        dock_widget = QWidget()
        dock_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name...")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_data)

        dock_layout.addWidget(self.search_input)
        dock_layout.addWidget(search_btn)
        dock_widget.setLayout(dock_layout)

        dock.setWidget(dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)

    def paste_clipboard(self):
        clipboard = QApplication.clipboard()
        self.name_input.setText(clipboard.text())

    def add_data(self):
        name = self.name_input.text()
        age = self.age_input.text()
        city = self.city_input.text()

        if name and age and city:
            self.data.append((name, age, city))
            self.refresh_table()
            self.clear_inputs()
        else:
            QMessageBox.warning(self, "Input Error", "All fields must be filled.")

    def update_data(self):
        if self.current_row != -1:
            name = self.name_input.text()
            age = self.age_input.text()
            city = self.city_input.text()
            self.data[self.current_row] = (name, age, city)
            self.refresh_table()
            self.clear_inputs()

    def delete_data(self):
        if self.current_row != -1:
            del self.data[self.current_row]
            self.refresh_table()
            self.clear_inputs()

    def load_row_data(self, row, _):
        self.current_row = row
        name, age, city = self.data[row]
        self.name_input.setText(name)
        self.age_input.setText(age)
        self.city_input.setText(city)

    def refresh_table(self):
        self.table.setRowCount(len(self.data))
        for row, (name, age, city) in enumerate(self.data):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(age))
            self.table.setItem(row, 2, QTableWidgetItem(city))
        self.current_row = -1

    def clear_inputs(self):
        self.name_input.clear()
        self.age_input.clear()
        self.city_input.clear()

    def search_data(self):
        keyword = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and keyword in item.text().lower():
                self.table.selectRow(row)
                return
        QMessageBox.information(self, "Not Found", "No matching name found.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CRUDApp()
    window.show()
    sys.exit(app.exec())
