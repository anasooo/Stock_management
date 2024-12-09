import sys
import os
import django
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QTableWidget, QTableWidgetItem, QPushButton, QWidget, 
                             QLabel, QLineEdit, QDialog, QFormLayout, QComboBox)  # Added QComboBox import
from PyQt5.QtCore import Qt

# Setup Django environment
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_management.settings")
django.setup()

# Import Django models
from inventory.models import Produit, Fournisseur, Client, Commande

class InventoryManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Tabs or sections
        self.setup_product_section(main_layout)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def setup_product_section(self, main_layout):
        # Product section label
        product_label = QLabel("Produits en Stock")
        main_layout.addWidget(product_label)

        # Product table
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(6)
        self.product_table.setHorizontalHeaderLabels([
            "ID", "Nom", "Référence", "Prix", "Quantité", "Fournisseur"
        ])
        main_layout.addWidget(self.product_table)

        # Buttons layout
        btn_layout = QHBoxLayout()
        
        # Add Product Button
        add_product_btn = QPushButton("Ajouter Produit")
        add_product_btn.clicked.connect(self.open_add_product_dialog)
        btn_layout.addWidget(add_product_btn)

        # Refresh Button
        refresh_btn = QPushButton("Actualiser")
        refresh_btn.clicked.connect(self.load_products)
        btn_layout.addWidget(refresh_btn)

        main_layout.addLayout(btn_layout)

        # Initially load products
        self.load_products()

    def load_products(self):
        # Clear existing items
        self.product_table.setRowCount(0)

        # Fetch products from Django model
        products = Produit.objects.all()

        # Populate table
        for row, product in enumerate(products):
            self.product_table.insertRow(row)
            
            # Add data to table
            self.product_table.setItem(row, 0, QTableWidgetItem(str(product.id)))
            self.product_table.setItem(row, 1, QTableWidgetItem(product.nom))
            self.product_table.setItem(row, 2, QTableWidgetItem(product.reference))
            self.product_table.setItem(row, 3, QTableWidgetItem(str(product.prix_unitaire)))
            self.product_table.setItem(row, 4, QTableWidgetItem(str(product.quantite_stock)))
            
            # Get fournisseur name safely
            fournisseur_name = product.fournisseur.nom if product.fournisseur else "N/A"
            self.product_table.setItem(row, 5, QTableWidgetItem(fournisseur_name))

    def open_add_product_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un Produit")
        
        layout = QFormLayout()
        
        # Input fields
        nom_input = QLineEdit()
        reference_input = QLineEdit()
        prix_input = QLineEdit()
        quantite_input = QLineEdit()
        
        # Fournisseur dropdown
        fournisseur_combo = QComboBox()  # Correctly imported
        fournisseurs = Fournisseur.objects.all()
        for fournisseur in fournisseurs:
            fournisseur_combo.addItem(fournisseur.nom, fournisseur.id)

        # Add inputs to layout
        layout.addRow("Nom:", nom_input)
        layout.addRow("Référence:", reference_input)
        layout.addRow("Prix Unitaire:", prix_input)
        layout.addRow("Quantité en Stock:", quantite_input)
        layout.addRow("Fournisseur:", fournisseur_combo)

        # Save button
        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(lambda: self.save_product(
            nom_input.text(), 
            reference_input.text(), 
            prix_input.text(), 
            quantite_input.text(), 
            fournisseur_combo.currentData()
        ))
        layout.addRow(save_btn)

        dialog.setLayout(layout)
        dialog.exec_()

    def save_product(self, nom, reference, prix, quantite, fournisseur_id):
        try:
            # Create new product
            fournisseur = Fournisseur.objects.get(id=fournisseur_id)
            Produit.objects.create(
                nom=nom,
                reference=reference,
                prix_unitaire=float(prix),
                quantite_stock=int(quantite),
                fournisseur=fournisseur
            )
            
            # Refresh product list
            self.load_products()
            
            # Close dialog
            self.sender().parent().close()
        except Exception as e:
            print(f"Erreur lors de l'ajout du produit: {e}")

def main():
    app = QApplication(sys.argv)
    main_window = InventoryManagementApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()