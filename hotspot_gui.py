import sys, time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont, QColor
import random
from helper_functions import scan_wifi_networks, process_network_list, count_empty_benches, print_bench_matrix, get_present_students, get_absent_students
from helper_functions import total_columns, total_rows

class AutoAttendanceSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Attendance System")
        self.setGeometry(100, 100, 600, 500)
        self.setFont(QFont("Times-New-Roman", 12))

        # Create the main widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        # Add the "Start Scanning" button
        self.start_scanning_button = QPushButton("Start Scanning")
        self.start_scanning_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 8px 16px;")
        self.main_layout.addWidget(self.start_scanning_button)

        self.table = QTableWidget()
        self.table.setColumnCount(10)  # number of columns in the table
        self.table.setRowCount(8)  # number of rows in the table
        self.table.horizontalHeader().hide()
        self.table.verticalHeader().hide()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("background-color: white; color: #555; font-size: 14px; padding: 8px;")
        self.main_layout.addWidget(self.table)

        # Add the present and absent lists
        self.lists_layout = QHBoxLayout()
        self.present_label = QLabel("Present:")
        self.present_label.setStyleSheet("font-size: 16px;")
        self.present_list = QTextEdit()
        self.present_list.setStyleSheet("background-color: #f2f2f2; color: #555; font-size: 14px; padding: 8px;")
        self.present_list.setReadOnly(True)
        self.absent_label = QLabel("Absent:")
        self.absent_label.setStyleSheet("font-size: 16px;")
        self.absent_list = QTextEdit()
        self.absent_list.setStyleSheet("background-color: #f2f2f2; color: #555; font-size: 14px; padding: 8px;")
        self.absent_list.setReadOnly(True)
        self.lists_layout.addWidget(self.present_label)
        self.lists_layout.addWidget(self.present_list)
        self.lists_layout.addWidget(self.absent_label)
        self.lists_layout.addWidget(self.absent_list)
        self.main_layout.addLayout(self.lists_layout)

        # Connect the "Start Scanning" button to the function that scans and updates the UI
        self.start_scanning_button.clicked.connect(self.scan_and_update_ui)

    def scan_and_update_ui(self):
       # TODO : Update the table with the matrix of seats

        # Update the table with the matrix of seats
      for row in range(total_rows):
        for col in range(total_columns):
            bench = (row+1, col+1)
            
            

            benches = {}
            """
            Creates an empty dictionary to store the number of students present at each bench.
            """

            network_list = scan_wifi_networks()
            """
            Scans for available Wi-Fi networks and returns a list of their names.
            """

            if network_list is None:
                break
            """
            If the scan returns an empty list, the loop breaks.
            """

            benches, filtered_network_list = process_network_list(network_list)
            """
            Processes the list of Wi-Fi networks and returns a dictionary that maps each network to a tuple of its coordinates.
            """

            empty_benches = count_empty_benches(benches, total_rows, total_columns)
            """
            Counts the number of empty benches in the dictionary.
            """

            print("Empty benches:", empty_benches)
            """
            Prints the number of empty benches.
            """

            # print_bench_matrix(benches)
            """
            Prints a matrix of the students present at each bench.
            """

            present_list = get_present_students(filtered_network_list)
            """
            Returns a list of the students present in a list of Wi-Fi networks.
            """

            print("Students present: ")
            print(present_list)
            """
            Prints a list of the students present.
            """

            absent_list = get_absent_students(present_list)

            # Set the text for the present and absent lists
            self.present_list.setPlainText("\n".join(str(num) for num in present_list))
            self.absent_list.setPlainText("\n".join(str(num) for num in absent_list))

            if bench in benches:
                count = benches[bench]['count']
                item = QTableWidgetItem("✓" if count==2 else "?" if count==1 else "")  # ? or ✓ in the cell
            
            else:
                item = QTableWidgetItem("X")  # set X in the cell

            item.setTextAlignment(4)  # center-align the text in the cell
            item.setFlags(item.flags() ^ 0x0001)  # make the cell non-editable
            self.table.setItem(row, col, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutoAttendanceSystem()
    window.show()
    sys.exit(app.exec_()) 










