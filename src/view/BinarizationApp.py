from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QSlider, QComboBox,
    QLineEdit, QGroupBox, QGridLayout, QMessageBox, QFrame,QApplication)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt,QTimer

import time


class BinarizationApp(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.image_path = None
        self.result = None
        self.image_selected = False
        self.image_label = QLabel()
        self.setWindowTitle("Binarization")
        self.setFixedSize(1000, 640)
        self.setStyleSheet("background-color: #cccccc")

        self.BUTTON_STYLE = """background-color: white;font: 12pt Arial;border-radius: 3px;padding: 7px;"""

        self.init_ui()

    def add_centered_widget(self, widget, width=235):
        widget.setFixedWidth(width)
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(widget)
        layout.addStretch()
        self.left_panel.addLayout(layout)

    def eventFilter(self, source, event):
        if source == self.select_button:
            if event.type() == event.Type.Enter:
                if self.image_selected:
                    self.select_button.setText("Выбрать другое")
            elif event.type() == event.Type.Leave:
                if not self.image_selected:
                    self.select_button.setText("Выбрать изображение")
                else:
                    self.select_button.setText(self.image_path.split("/")[-1])
        return super().eventFilter(source, event)

    def init_ui(self):
        self.init_main_layout()
        self.init_left_panel()
        self.init_method_controls()
        self.init_global_method_box()
        self.init_eikwel_box()
        self.init_niblack_box()
        self.init_buttons()
        self.init_image_frame()
        self.apply_styles()

    def apply_styles(self):
        self.select_button.setStyleSheet(self.BUTTON_STYLE)
        self.process_button.setStyleSheet(self.BUTTON_STYLE)
        self.save_button.setStyleSheet(self.BUTTON_STYLE)
        self.exit_button.setStyleSheet(self.BUTTON_STYLE)

    def init_main_layout(self):
        self.main_layout = QHBoxLayout(self)

    def init_left_panel(self):
        self.left_panel = QVBoxLayout()
        self.left_panel.setSpacing(15)
        self.left_panel.setContentsMargins(0, 10, 0, 10)

        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left_panel)
        self.left_widget.setFixedWidth(250)
        self.left_widget.setFixedHeight(615)
        self.left_widget.setStyleSheet("""
            background-color: #f0f0f0;
            border-radius: 3px;
        """)

        self.main_layout.addWidget(self.left_widget)

    def init_method_controls(self):
        self.select_button = QPushButton("Выбрать изображение")
        self.select_button.installEventFilter(self)

        self.select_button.clicked.connect(self.on_load_click)
        self.add_centered_widget(self.select_button)

        self.method_menu = QComboBox()
        self.method_menu.setEnabled(False)
        self.method_menu.setPlaceholderText("Выбрать метод")
        self.method_menu.addItems([
            "Глобальный", "Оцу", "Бернсена", "Ниблэка",
            "Саувола", "Кристиана", "Эйквеля", "Брэдли"
        ])
        self.method_menu.currentTextChanged.connect(self.on_method_change)
        self.method_menu.setStyleSheet("""
            QComboBox {font: 12pt Arial;padding: 7px;border-radius: 3px;background-color: white;}
            QComboBox::drop-down {width: 20px;border-left: 2px solid #bdc3c7;}
            QComboBox QAbstractItemView {background-color: white;}
        """)
        self.add_centered_widget(self.method_menu)

    def init_global_method_box(self):
        self.global_box = QGroupBox()
        layout = QVBoxLayout()

        self.slider_label = QLabel("пороговое значение: 128")
        self.slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.slider_label.setStyleSheet("font: 11pt Arial;")
        layout.addWidget(self.slider_label)

        self.thresh_slider = QSlider(Qt.Orientation.Horizontal)
        self.thresh_slider.setMinimum(0)
        self.thresh_slider.setMaximum(255)
        self.thresh_slider.setValue(128)
        self.thresh_slider.setEnabled(False)
        self.thresh_slider.valueChanged.connect(
            lambda val: self.slider_label.setText(f"пороговое значение: {val}")
        )
        layout.addWidget(self.thresh_slider)

        self.global_box.setLayout(layout)
        self.global_box.hide()
        self.add_centered_widget(self.global_box)

    def init_eikwel_box(self):
        self.eikwel_box = QGroupBox()
        layout = QGridLayout()

        self.r_size_input = QLineEdit()
        self.R_size_input = QLineEdit()
        self.eps_input = QLineEdit()
        for w in [self.r_size_input, self.R_size_input, self.eps_input]:
            w.setStyleSheet("background-color: white;")
            w.textChanged.connect(self.check_params)

        layout.addWidget(QLabel("r_size:"), 0, 0)
        layout.addWidget(self.r_size_input, 0, 1)
        layout.addWidget(QLabel("R_size:"), 1, 0)
        layout.addWidget(self.R_size_input, 1, 1)
        layout.addWidget(QLabel("eps:"), 2, 0)
        layout.addWidget(self.eps_input, 2, 1)

        self.eikwel_box.setLayout(layout)
        self.eikwel_box.hide()
        self.left_panel.addWidget(self.eikwel_box)

    def init_niblack_box(self):
        self.niblack_box = QGroupBox()
        layout = QGridLayout()

        self.window_input = QLineEdit("15")
        self.k_input = QLineEdit("0.2")
        for w in [self.window_input, self.k_input]:
            w.setStyleSheet("background-color: white;")
            w.textChanged.connect(self.check_params)

        layout.addWidget(QLabel("window:"), 0, 0)
        layout.addWidget(self.window_input, 0, 1)
        layout.addWidget(QLabel("k-param:"), 1, 0)
        layout.addWidget(self.k_input, 1, 1)

        self.niblack_box.setLayout(layout)
        self.niblack_box.hide()
        self.left_panel.addWidget(self.niblack_box)

    def init_buttons(self):
        self.left_panel.addStretch()

        self.process_button = QPushButton("Обработать")

        self.process_button.setEnabled(False)
        self.process_button.clicked.connect(self.on_process_click)
        self.add_centered_widget(self.process_button)

        self.save_button = QPushButton("Сохранить")

        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.on_save_click)
        self.add_centered_widget(self.save_button)

        self.exit_button = QPushButton("Выход")

        self.exit_button.clicked.connect(self.close)
        self.add_centered_widget(self.exit_button)

    def init_image_frame(self):
        self.image_frame = QFrame()
        self.image_frame.setStyleSheet("background-color: #2c2c2c; border-radius: 3px")
        self.image_frame.setFixedSize(700, 615)

        layout = QVBoxLayout(self.image_frame)
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.image_frame)

    @property
    def ui_elements(self):
        return {
            "thresh_slider": self.thresh_slider,
            "r_size_input": self.r_size_input,
            "R_size_input": self.R_size_input,
            "eps_input": self.eps_input,
            "window_input": self.window_input,
            "k_input": self.k_input,
        }

    @property
    def method_name(self):
        return self.method_menu.currentText()

    def on_load_click(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg *.webp)")
        if path:
            self.image_path = path
            image = self.controller.load_image(path)
            if image is not None:
                self.image_selected = True
                self.select_button.setText(path.split("/")[-1])
                self.method_menu.setEnabled(True)
                self.show_image(image)
            else:
                QMessageBox.critical(self, "Ошибка", "Не удалось загрузить изображение.")

    def on_method_change(self, method):
        self.global_box.hide()
        self.eikwel_box.hide()
        self.niblack_box.hide()
        self.process_button.setEnabled(True)

        if method == "Глобальный":
            self.global_box.show()
            self.thresh_slider.setEnabled(True)
        elif method == "Эйквеля":
            self.eikwel_box.show()
            self.process_button.setEnabled(False)
            self.check_params()
        elif method in ["Ниблэка", "Саувола", "Кристиана"]:
            self.niblack_box.show()
            self.process_button.setEnabled(False)
            self.check_params()

    def check_params(self):
        params = self.controller.collect_params(self.method_name, self.ui_elements)
        self.process_button.setEnabled(self.controller.validate_method_params(self.method_name, params))

    def on_process_click(self):
        self.process_button.setText("Загрузка...")
        self.process_button.setEnabled(False)
        QApplication.processEvents()

        params = self.controller.collect_params(self.method_name, self.ui_elements)
        if not self.controller.validate_method_params(self.method_name, params):
            self.process_button.setText("Обработать")
            self.process_button.setEnabled(True)
            return

        start_time = time.perf_counter()

        result = self.controller.apply_method(self.method_name, params)

        end_time = time.perf_counter()
        duration = end_time - start_time 

        print(f"{self.method_name}: {duration:.3f} сек")

        if result is not None:
            self.result = result
            self.save_button.setEnabled(True)
            self.show_image(result)

        self.process_button.setText("Обработать")
        QTimer.singleShot(1000, lambda: self.process_button.setEnabled(True))

    def on_save_click(self):
        if self.result is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "", "Images (*.jpg *.jpeg *.png)")
            if file_path:
                self.controller.save_result(file_path)

    def show_image(self, image_array):
        h, w = image_array.shape[:2]
        if len(image_array.shape) == 3:
            qimage = QImage(image_array.data, w, h, 3 * w, QImage.Format.Format_RGB888)
        else:
            qimage = QImage(image_array.data, w, h, w, QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimage)

        max_width = 670
        max_height = 585

        if w > max_width or h > max_height:
            pixmap = pixmap.scaled(
                max_width, max_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
