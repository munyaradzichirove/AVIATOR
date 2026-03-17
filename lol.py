import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QPushButton, QLineEdit, 
                             QLabel, QFrame, QComboBox, QScrollArea)
from PyQt6.QtCore import Qt

class POSApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Retail POS Dashboard")
        self.showMaximized()
        self.setStyleSheet("background-color: #f4f7f9; font-family: 'Segoe UI', Arial;")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- 1. LEFT CATEGORIES SIDEBAR ---
        sidebar = QFrame()
        sidebar.setFixedWidth(160) # Narrower to give more room to center/cart
        sidebar.setStyleSheet("background-color: #f0f2f5; border-right: 1px solid #dee2e6;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(5, 5, 5, 5)
        sidebar_layout.setSpacing(2)
        
        cat_title = QLabel("Categories")
        cat_title.setStyleSheet("font-weight: bold; font-size: 16px; padding: 10px; color: #333;")
        sidebar_layout.addWidget(cat_title)

        categories = [
            ("All Item Groups", "2 items", "#004d26"),
            ("BABY CARE", "52 items", "#6a0dad"),
            ("BABY MILK", "2 items", "#6a0dad"),
            ("BAKERY INGREDIENTS", "39 items", "#635a31"),
            ("BAKERY BREAD", "10 items", "#800080"),
            ("BAKERY CONFECTIONERY", "26 items", "#2a004d"),
            ("BEARING HOUSING", "1 item", "#99004d"),
        ]

        for name, count, color in categories:
            btn = QPushButton(f"{name}\n{count}")
            btn.setFixedHeight(70)
            btn.setStyleSheet(f"background-color: {color}; color: white; border: none; text-align: left; padding: 8px; font-weight: bold; font-size: 10px;")
            sidebar_layout.addWidget(btn)
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # --- 2. CENTER PRODUCT GRID ---
        center_section = QWidget()
        center_layout = QVBoxLayout(center_section)
        center_layout.setContentsMargins(10, 10, 10, 10)

        # Header with Dropdowns
        header = QHBoxLayout()
        header.addWidget(QLabel("<h2>BAKERY INGREDIENTS</h2>"))
        header.addStretch()
        for text in ["Sales Invoice", "Select agent", "Select customer"]:
            cb = QComboBox()
            cb.addItem(text)
            cb.setStyleSheet("background: white; border: 1px solid #ccc; padding: 4px;")
            header.addWidget(cb)
        center_layout.addLayout(header)

        # Search
        search = QLineEdit()
        search.setPlaceholderText("Search or scan barcode...")
        search.setStyleSheet("background: white; border: 1px solid #ccc; padding: 8px; margin-bottom: 5px;")
        center_layout.addWidget(search)

        # Grid with REDUCED SPACING
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        grid_container = QWidget()
        grid = QGridLayout(grid_container)
        grid.setSpacing(4) # <--- Reduced margin between items
        grid.setContentsMargins(0, 0, 0, 0)
        
        items = ["KEFALOS CHEESE", "BAKERY SPONGE ORANGE 8\"", "BAKERY BIRDS EYE CHILLIES", 
                 "BAKERY SOLEN AMADA", "DAIRIBORD FUN N FRESH", "BAKERY CHUNKS KG", 
                 "CAKE SLICE DOOM EACH", "VINOPHANE 300*380MM", "CAKE DOME LARGE", "POLYPROP ROLL KG"]
        
        for i in range(40): # Fill grid
            name = items[i % len(items)]
            item_btn = QPushButton(name)
            item_btn.setFixedSize(145, 75)
            
            # Highlight specific item logic
            is_doom = "DOOM" in name
            border = "#4fd1c5" if is_doom else "#dee2e6"
            bg = "#e6fffa" if is_doom else "white"
            
            item_btn.setStyleSheet(f"background-color: {bg}; border: 1px solid {border}; border-radius: 2px; color: #333; font-size: 10px; font-weight: bold; text-align: center;")
            grid.addWidget(item_btn, i // 5, i % 5)
        
        scroll.setWidget(grid_container)
        center_layout.addWidget(scroll)
        main_layout.addWidget(center_section, stretch=5)

        # --- 3. INCREASED CART WIDTH ---
        receipt = QFrame()
        receipt.setFixedWidth(450) # <--- Increased from 300 to 450
        receipt.setStyleSheet("background-color: white; border-left: 1px solid #dee2e6;")
        receipt_layout = QVBoxLayout(receipt)
        
        # Header Info (Invoice & Clock)
        header_info = QLabel("<span style='color:green;'>Invoice: ACC-SINV-2026-00437</span><br><h1 style='margin:0;'>16:09:53</h1><br>March 13, 2026")
        header_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        receipt_layout.addWidget(header_info)
        
        # Stats Row (Total, Paid, Change)
        stats = QHBoxLayout()
        for label in ["Total<br>$5.00", "Paid<br>$5.00", "Change<br>$0.00"]:
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-size: 11px; font-weight: bold; border-right: 1px solid #eee;")
            stats.addWidget(lbl)
        receipt_layout.addLayout(stats)
        
        receipt_layout.addSpacing(50)
        cart_empty = QLabel("🛒<br>Cart is empty")
        cart_empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cart_empty.setStyleSheet("color: #ccc; font-size: 20px;")
        receipt_layout.addWidget(cart_empty)
        
        receipt_layout.addStretch()

        # Bottom Button
        pay_btn = QPushButton("Place Order (F10)")
        pay_btn.setFixedHeight(50)
        pay_btn.setStyleSheet("background-color: #81e6d9; border: none; font-weight: bold; font-size: 16px; color: #2c7a7b;")
        receipt_layout.addWidget(pay_btn)
        
        main_layout.addWidget(receipt)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = POSApp()
    window.show()
    sys.exit(app.exec())