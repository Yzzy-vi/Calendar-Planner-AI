import sys
import os
import json
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QSizePolicy, QTextEdit, QFileDialog, QLineEdit, QScrollArea
)
from PyQt6.QtGui import QPixmap, QMouseEvent, QFont
from PyQt6.QtCore import Qt, QPoint, QElapsedTimer

# Load API keys with fallback
config = {}
try:
    with open("config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    print("Warning: config.json not found. Background search will use placeholder colors.")
    config = {"background_api_key": ""}

MEDIA_FOLDER = "media_pages"
DATA_FILE = "media_data.json"
DEFAULT_BACKGROUND = "lightgray"  # Default background color

class MediaEditor(QWidget):
    def __init__(self, page_id):
        super().__init__()
        self.setWindowTitle(f"Edit Page {page_id}")
        self.resize(400, 400)
        self.page_id = page_id

        self.layout = QVBoxLayout()
        self.note_edit = QTextEdit()
        self.image_label = QLabel("No media")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedHeight(200)

        self.upload_btn = QPushButton("Upload Media")
        self.save_btn = QPushButton("Save")

        self.upload_btn.clicked.connect(self.upload_media)
        self.save_btn.clicked.connect(self.save_data)

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.upload_btn)
        self.layout.addWidget(self.note_edit)
        self.layout.addWidget(self.save_btn)
        self.setLayout(self.layout)

        self.media_path = None
        self.load_data()

    def upload_media(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Media", "", "Images (*.png *.jpg *.jpeg)")
        if file:
            self.media_path = file
            pixmap = QPixmap(file).scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                if str(self.page_id) in data:
                    self.note_edit.setPlainText(data[str(self.page_id)].get("note", ""))
                    media_path = data[str(self.page_id)].get("media")
                    if media_path and os.path.exists(media_path):
                        pixmap = QPixmap(media_path).scaled(300, 200, Qt.AspectRatioMode.KeepAspectRatio)
                        self.image_label.setPixmap(pixmap)
                        self.media_path = media_path

    def save_data(self):
        note = self.note_edit.toPlainText()
        data = {}
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f) if os.path.getsize(DATA_FILE) > 0 else {}

        data[str(self.page_id)] = {
            "note": note,
            "media": self.media_path
        }

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
        self.close()

class MediaReelWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_page = 0
        self.total_pages = len([f for f in os.listdir(MEDIA_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]) if os.path.exists(MEDIA_FOLDER) and os.path.isdir(MEDIA_FOLDER) else 0
        self.background_url = None

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.layout)
        self.setStyleSheet(f"QWidget {{ background-color: {DEFAULT_BACKGROUND}; }}")

        # Search bar for backgrounds
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search backgrounds...")
        self.search_bar.returnPressed.connect(self.perform_search)
        self.layout.addWidget(self.search_bar)

        # Search results area
        self.results_area = QScrollArea()
        self.results_content = QWidget()
        self.results_layout = QHBoxLayout(self.results_content)
        self.results_area.setWidget(self.results_content)
        self.results_area.setWidgetResizable(True)
        self.layout.addWidget(self.results_area, stretch=1)

        # Media display
        self.media_label = QLabel()
        self.media_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.media_label)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("◀ Prev")
        self.next_btn = QPushButton("Next ▶")
        self.edit_btn = QPushButton("Edit")
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.edit_btn.clicked.connect(self.edit_page)
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.edit_btn)
        nav_layout.addWidget(self.next_btn)
        self.layout.addLayout(nav_layout)

        self.load_page(self.current_page)

    def load_page(self, index):
        if self.total_pages > 0:
            files = [f for f in os.listdir(MEDIA_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]
            if 0 <= index < len(files):
                path = os.path.join(MEDIA_FOLDER, files[index])
                pixmap = QPixmap(path).scaled(600, 400, Qt.AspectRatioMode.KeepAspectRatio)
                self.media_label.setPixmap(pixmap)
                self.media_label.setFixedSize(pixmap.size())
            else:
                self.media_label.setText(f"Page {index + 1} not found")
        else:
            self.media_label.setText("No media pages found in 'media_pages' folder.")

        # Load notes from data file
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                if str(index) in data:
                    note = data[str(index)].get("note", "")
                    if note:
                        self.media_label.setText(f"Note: {note}")

    def prev_page(self):
        if self.total_pages > 0:
            self.current_page = (self.current_page - 1) % self.total_pages
            self.load_page(self.current_page)

    def next_page(self):
        if self.total_pages > 0:
            self.current_page = (self.current_page + 1) % self.total_pages
            self.load_page(self.current_page)

    def edit_page(self):
        editor = MediaEditor(self.current_page)
        editor.exec()

    def perform_search(self):
        term = self.search_bar.text()
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if config.get("background_api_key"):
            try:
                # Placeholder for API call (e.g., Unsplash)
                print(f"Searching for {term} with API (key required)")
                # Replace with actual API endpoint and key
            except Exception as e:
                print(f"Background API error: {e}")
        else:
            # Fallback to placeholder colors
            if term:
                for color in ["red", "blue", "green", "lightgray"]:
                    if term.lower() in color:
                        label = QLabel()
                        label.setStyleSheet(f"background-color: {color};")
                        label.setFixedSize(150, 100)
                        label.mousePressEvent = lambda e, c=color: self.set_background(c)
                        self.results_layout.addWidget(label)

    def set_background(self, color):
        self.setStyleSheet(f"QWidget {{ background-color: {color}; }}")

class MediaReelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Reel App")
        self.setMinimumSize(600, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().availableGeometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout(self.central)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.reel_widget = MediaReelWidget()
        self.layout.addWidget(self.reel_widget)

        self.make_close_button()

        # Drag/resize helpers
        self.timer = QElapsedTimer()
        self.start_pos = QPoint()
        self.global_start = QPoint()
        self.dragging = False
        self.resizing = False
        self.resize_edge = None
        self.resize_margin = 10

    def make_close_button(self):
        self.close_btn = QPushButton("✖", self)
        self.close_btn.setFixedSize(40, 40)
        self.close_btn.move(self.width() - 60, 20)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-weight: bold;
                border-radius: 20px;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        self.close_btn.raise_()
        self.close_btn.show()

    def detect_resize_zone(self, pos: QPoint):
        rect = self.rect()
        x, y = pos.x(), pos.y()
        margin = self.resize_margin

        if rect.width() - margin < x < rect.width() and rect.height() - margin < y < rect.height():
            return 'corner'
        elif rect.width() - margin < x < rect.width():
            return 'right'
        elif rect.height() - margin < y < rect.height():
            return 'bottom'
        return None

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            edge = self.detect_resize_zone(event.position().toPoint())
            if edge:
                self.resizing = True
                self.resize_edge = edge
            else:
                self.timer.start()
                self.dragging = True
                self.start_pos = event.position().toPoint()
                self.global_start = event.globalPosition().toPoint()
        event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.resizing:
            delta = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            if self.resize_edge == 'right':
                self.resize(max(600, delta.x()), self.height())
            elif self.resize_edge == 'bottom':
                self.resize(self.width(), max(800, delta.y()))
            elif self.resize_edge == 'corner':
                self.resize(max(600, delta.x()), max(800, delta.y()))
        elif self.dragging:
            delta_t = self.timer.elapsed()
            delta = event.globalPosition().toPoint() - self.global_start
            if delta_t > 200 and delta.manhattanLength() > 10:
                self.move(event.globalPosition().toPoint() - self.start_pos)
        else:
            edge = self.detect_resize_zone(event.position().toPoint())
            if edge == 'corner':
                self.setCursor(Qt.CursorShape.SizeFDiagCursor)
            elif edge == 'right':
                self.setCursor(Qt.CursorShape.SizeHorCursor)
            elif edge == 'bottom':
                self.setCursor(Qt.CursorShape.SizeVerCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)
        event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.resizing:
            self.resizing = False
            self.resize_edge = None
        elif self.dragging:
            delta_x = event.position().x() - self.start_pos.x()
            delta_t = self.timer.elapsed()
            if delta_t < 200 and abs(delta_x) > 50:
                if delta_x > 0:
                    self.reel_widget.prev_page()
                else:
                    self.reel_widget.next_page()
            self.dragging = False
        event.accept()

    def resizeEvent(self, event):
        self.close_btn.move(self.width() - 60, 20)
        self.reel_widget.load_page(self.reel_widget.current_page)
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MediaReelApp()
    window.show()
    sys.exit(app.exec())