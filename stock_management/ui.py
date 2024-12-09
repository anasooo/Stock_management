import sys
import os
import django
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QTableWgedt, QTableWidgetItem, QPushButton, QWidget,
                            QLabel, QLineEdit, QDialog, QFormLayout)
from PyQt5.QtCore import Qt

# Set up Django env
sys.path.append(os.path.join(os.path.dirname(__file__), 'stock_management'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stock_management.settings')
django.setup()
