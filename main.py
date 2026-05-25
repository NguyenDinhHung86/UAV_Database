import sys
import json
import os
import numpy as np
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLineEdit, QPushButton, QLabel,
    QComboBox, QSplitter, QTabWidget, QFormLayout, QDoubleSpinBox,
    QSpinBox, QTextEdit, QMessageBox, QHeaderView, QFrame,
    QScrollArea, QCheckBox, QGroupBox, QDialog, QDialogButtonBox,
    QSizePolicy, QStackedWidget
)
from PyQt6.QtCore import Qt, QSortFilterProxyModel, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon, QPixmap

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from database import UAVDatabase
from uav_model import UAV

# ─────────────────────────── Styles ────────────────────────────
DARK_STYLE = """
QMainWindow, QDialog {
    background-color: #1a1d23;
    color: #e0e0e0;
}
QWidget {
    background-color: #1a1d23;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}
QTableWidget {
    background-color: #22262e;
    alternate-background-color: #262b33;
    color: #e0e0e0;
    gridline-color: #2e3340;
    border: 1px solid #2e3340;
    border-radius: 6px;
    selection-background-color: #2a5298;
}
QTableWidget::item:selected {
    background-color: #2a5298;
    color: #ffffff;
}
QHeaderView::section {
    background-color: #2e3340;
    color: #a0b0cc;
    padding: 8px 12px;
    border: none;
    border-right: 1px solid #3a4050;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #22262e;
    color: #e0e0e0;
    border: 1px solid #3a4050;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 13px;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border: 1px solid #4a7fc1;
    background-color: #262b38;
}
QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #22262e;
    color: #e0e0e0;
    border: 1px solid #3a4050;
    selection-background-color: #2a5298;
}
QPushButton {
    background-color: #2a5298;
    color: #ffffff;
    border: none;
    border-radius: 6px;
    padding: 8px 18px;
    font-weight: 600;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #3466b8;
}
QPushButton:pressed {
    background-color: #1e3d73;
}
QPushButton.danger {
    background-color: #8b2020;
}
QPushButton.danger:hover {
    background-color: #a82828;
}
QPushButton.secondary {
    background-color: #2e3340;
    color: #a0b0cc;
}
QPushButton.secondary:hover {
    background-color: #3a4050;
    color: #e0e0e0;
}
QPushButton.success {
    background-color: #1a6b3a;
}
QPushButton.success:hover {
    background-color: #228048;
}
QTabWidget::pane {
    border: 1px solid #2e3340;
    border-radius: 6px;
    background-color: #1e2230;
}
QTabBar::tab {
    background-color: #22262e;
    color: #8090a8;
    padding: 9px 20px;
    border: none;
    border-bottom: 2px solid transparent;
    font-size: 13px;
    font-weight: 500;
}
QTabBar::tab:selected {
    color: #4a9eff;
    border-bottom: 2px solid #4a9eff;
    background-color: #1e2230;
}
QTabBar::tab:hover {
    color: #c0d0e8;
    background-color: #262b38;
}
QGroupBox {
    border: 1px solid #2e3340;
    border-radius: 8px;
    margin-top: 16px;
    padding: 12px;
    font-weight: 600;
    color: #8090a8;
    font-size: 12px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #6090cc;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
QScrollBar:vertical {
    background: #1a1d23;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #3a4050;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #4a5060;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
QLabel#title {
    font-size: 22px;
    font-weight: 700;
    color: #e8f0ff;
}
QLabel#subtitle {
    font-size: 13px;
    color: #6080a0;
}
QLabel#stat_value {
    font-size: 24px;
    font-weight: 700;
    color: #4a9eff;
}
QLabel#stat_label {
    font-size: 11px;
    color: #6080a0;
    text-transform: uppercase;
}
QFrame#stat_card {
    background-color: #22262e;
    border: 1px solid #2e3340;
    border-radius: 10px;
    padding: 12px;
}
QFrame#divider {
    background-color: #2e3340;
    max-height: 1px;
}
QCheckBox {
    color: #a0b0cc;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border: 1px solid #3a4050;
    border-radius: 4px;
    background-color: #22262e;
}
QCheckBox::indicator:checked {
    background-color: #2a5298;
    border-color: #4a7fc1;
}
QSplitter::handle {
    background-color: #2e3340;
    width: 2px;
}
"""

# ─────────────────────────── RF Chart Widget ────────────────────────────
class RFChartWidget(FigureCanvas):
    def __init__(self, parent=None, dark=True):
        self.fig = Figure(figsize=(6, 3.5), facecolor='#1e2230')
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.dark = dark
        self._draw_empty()

    def _draw_empty(self):
        self.fig.clear()
        ax = self.fig.add_subplot(111, facecolor='#1e2230')
        ax.text(0.5, 0.5, 'Chọn UAV để xem biểu đồ RF',
                ha='center', va='center', color='#506080',
                fontsize=13, transform=ax.transAxes)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color('#2e3340')
        self.fig.tight_layout()
        self.draw()

    def plot_rf(self, uav: 'UAV'):
        self.fig.clear()
        self.fig.patch.set_facecolor('#1e2230')

        freq_center = uav.freq_center_mhz or 2400
        bw = uav.freq_bandwidth_mhz or 80
        snr = uav.snr_db or 20
        freq_hop = uav.freq_hopping

        freqs = np.linspace(freq_center - bw * 1.5, freq_center + bw * 1.5, 1000)
        np.random.seed(hash(uav.name) % (2**32))

        # Simulated PSD
        signal = np.exp(-0.5 * ((freqs - freq_center) / (bw / 3))**2)
        noise_floor = 10 ** (-snr / 20)
        noise = noise_floor * np.abs(np.random.randn(len(freqs))) * 0.3
        psd_db = 10 * np.log10(signal + noise + 1e-6)

        # STFT-like spectrogram simulation
        t_points = 80
        t = np.linspace(0, 1, t_points)
        spec = np.zeros((len(freqs)//4, t_points))
        f_sub = freqs[::4]

        for ti in range(t_points):
            if freq_hop:
                hop_offset = np.sin(2 * np.pi * 3 * t[ti]) * bw * 0.4
                sig_t = np.exp(-0.5 * ((f_sub - (freq_center + hop_offset)) / (bw / 5))**2)
            else:
                sig_t = np.exp(-0.5 * ((f_sub - freq_center) / (bw / 3))**2)
            noise_t = noise_floor * np.abs(np.random.randn(len(f_sub))) * 0.2
            spec[:, ti] = 10 * np.log10(sig_t + noise_t + 1e-6)

        ax1 = self.fig.add_subplot(211, facecolor='#1a1d27')
        ax1.plot(freqs, psd_db, color='#4a9eff', linewidth=1.2, alpha=0.9)
        ax1.fill_between(freqs, psd_db, psd_db.min(), alpha=0.15, color='#4a9eff')
        ax1.axvline(freq_center, color='#ff6b6b', linewidth=1, linestyle='--', alpha=0.7)
        ax1.set_title(f'Power Spectral Density — {uav.name}', color='#c0d0e8', fontsize=11, pad=8)
        ax1.set_xlabel('Frequency (MHz)', color='#6080a0', fontsize=9)
        ax1.set_ylabel('Power (dBm)', color='#6080a0', fontsize=9)
        ax1.tick_params(colors='#6080a0', labelsize=8)
        for spine in ax1.spines.values():
            spine.set_color('#2e3340')
        ax1.grid(True, color='#2e3340', alpha=0.5, linewidth=0.5)

        ax2 = self.fig.add_subplot(212, facecolor='#1a1d27')
        im = ax2.imshow(spec, aspect='auto', origin='lower',
                        extent=[0, 1, f_sub[0], f_sub[-1]],
                        cmap='plasma', vmin=-30, vmax=0)
        ax2.set_title('Spectrogram (STFT)', color='#c0d0e8', fontsize=11, pad=8)
        ax2.set_xlabel('Time (normalized)', color='#6080a0', fontsize=9)
        ax2.set_ylabel('Frequency (MHz)', color='#6080a0', fontsize=9)
        ax2.tick_params(colors='#6080a0', labelsize=8)
        for spine in ax2.spines.values():
            spine.set_color('#2e3340')
        cbar = self.fig.colorbar(im, ax=ax2, fraction=0.03, pad=0.02)
        cbar.ax.tick_params(colors='#6080a0', labelsize=8)
        cbar.set_label('dBm', color='#6080a0', fontsize=8)

        self.fig.tight_layout(pad=1.5)
        self.draw()

    def plot_comparison(self, uavs: list):
        self.fig.clear()
        self.fig.patch.set_facecolor('#1e2230')
        if not uavs:
            self._draw_empty()
            return

        colors = ['#4a9eff', '#ff6b6b', '#51cf66', '#ffd43b', '#cc5de8', '#ff922b']
        ax = self.fig.add_subplot(111, facecolor='#1a1d27')

        for i, uav in enumerate(uavs):
            freq_center = uav.freq_center_mhz or 2400
            bw = uav.freq_bandwidth_mhz or 80
            snr = uav.snr_db or 20
            freqs = np.linspace(freq_center - bw * 2, freq_center + bw * 2, 800)
            np.random.seed(hash(uav.name) % (2**32))
            signal = np.exp(-0.5 * ((freqs - freq_center) / (bw / 3))**2)
            noise = (10**(-snr/20)) * np.abs(np.random.randn(len(freqs))) * 0.2
            psd = 10 * np.log10(signal + noise + 1e-6)
            c = colors[i % len(colors)]
            ax.plot(freqs, psd, color=c, linewidth=1.4, label=uav.name, alpha=0.85)
            ax.fill_between(freqs, psd, psd.min(), alpha=0.06, color=c)

        ax.set_title('So sánh phổ RF giữa các UAV', color='#c0d0e8', fontsize=11, pad=8)
        ax.set_xlabel('Frequency (MHz)', color='#6080a0', fontsize=9)
        ax.set_ylabel('Power (dBm)', color='#6080a0', fontsize=9)
        ax.tick_params(colors='#6080a0', labelsize=8)
        for spine in ax.spines.values():
            spine.set_color('#2e3340')
        ax.grid(True, color='#2e3340', alpha=0.5, linewidth=0.5)
        leg = ax.legend(facecolor='#22262e', edgecolor='#3a4050',
                        labelcolor='#c0d0e8', fontsize=9)
        self.fig.tight_layout(pad=1.5)
        self.draw()


# ─────────────────────────── UAV Form Dialog ────────────────────────────
class UAVFormDialog(QDialog):
    def __init__(self, parent=None, uav: 'UAV' = None):
        super().__init__(parent)
        self.uav = uav
        self.setWindowTitle("Thêm UAV mới" if uav is None else f"Chỉnh sửa — {uav.name}")
        self.setMinimumWidth(560)
        self.setStyleSheet(DARK_STYLE)
        self._build_ui()
        if uav:
            self._populate(uav)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Thêm UAV mới" if self.uav is None else "Chỉnh sửa UAV")
        title.setObjectName("title")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        divider = QFrame(); divider.setObjectName("divider"); divider.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(divider)

        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame)
        container = QWidget()
        form_layout = QVBoxLayout(container)
        form_layout.setSpacing(10)

        # ── Basic Info ──
        g1 = QGroupBox("Thông tin cơ bản")
        f1 = QFormLayout(g1); f1.setSpacing(8)
        self.name_edit = QLineEdit(); self.name_edit.setPlaceholderText("Ví dụ: DJI Phantom 4")
        self.manufacturer_edit = QLineEdit(); self.manufacturer_edit.setPlaceholderText("Ví dụ: DJI")
        self.model_edit = QLineEdit(); self.model_edit.setPlaceholderText("Ví dụ: Phantom 4 Pro V2")
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Consumer", "Professional", "Military", "Racing", "Agricultural", "Research", "Industrial"])
        self.year_spin = QSpinBox(); self.year_spin.setRange(2000, 2030); self.year_spin.setValue(2023)
        f1.addRow("Tên UAV *", self.name_edit)
        f1.addRow("Hãng sản xuất", self.manufacturer_edit)
        f1.addRow("Model", self.model_edit)
        f1.addRow("Danh mục", self.category_combo)
        f1.addRow("Năm sản xuất", self.year_spin)
        form_layout.addWidget(g1)

        # ── Technical Specs ──
        g2 = QGroupBox("Thông số kỹ thuật")
        f2 = QFormLayout(g2); f2.setSpacing(8)
        self.weight_spin = QDoubleSpinBox(); self.weight_spin.setRange(0, 50000); self.weight_spin.setSuffix(" g"); self.weight_spin.setDecimals(1)
        self.max_speed_spin = QDoubleSpinBox(); self.max_speed_spin.setRange(0, 500); self.max_speed_spin.setSuffix(" km/h"); self.max_speed_spin.setDecimals(1)
        self.max_altitude_spin = QSpinBox(); self.max_altitude_spin.setRange(0, 10000); self.max_altitude_spin.setSuffix(" m")
        self.flight_time_spin = QSpinBox(); self.flight_time_spin.setRange(0, 300); self.flight_time_spin.setSuffix(" phút")
        self.range_spin = QDoubleSpinBox(); self.range_spin.setRange(0, 200); self.range_spin.setSuffix(" km"); self.range_spin.setDecimals(1)
        self.battery_spin = QSpinBox(); self.battery_spin.setRange(0, 30000); self.battery_spin.setSuffix(" mAh")
        f2.addRow("Trọng lượng", self.weight_spin)
        f2.addRow("Tốc độ tối đa", self.max_speed_spin)
        f2.addRow("Độ cao tối đa", self.max_altitude_spin)
        f2.addRow("Thời gian bay", self.flight_time_spin)
        f2.addRow("Tầm hoạt động", self.range_spin)
        f2.addRow("Pin", self.battery_spin)
        form_layout.addWidget(g2)

        # ── RF Parameters ──
        g3 = QGroupBox("Thông số RF (tín hiệu vô tuyến)")
        f3 = QFormLayout(g3); f3.setSpacing(8)
        self.freq_center_spin = QDoubleSpinBox(); self.freq_center_spin.setRange(100, 6000); self.freq_center_spin.setSuffix(" MHz"); self.freq_center_spin.setValue(2400); self.freq_center_spin.setDecimals(1)
        self.freq_bw_spin = QDoubleSpinBox(); self.freq_bw_spin.setRange(0.1, 500); self.freq_bw_spin.setSuffix(" MHz"); self.freq_bw_spin.setValue(80); self.freq_bw_spin.setDecimals(1)
        self.snr_spin = QDoubleSpinBox(); self.snr_spin.setRange(-30, 60); self.snr_spin.setSuffix(" dB"); self.snr_spin.setValue(20); self.snr_spin.setDecimals(1)
        self.tx_power_spin = QSpinBox(); self.tx_power_spin.setRange(-20, 50); self.tx_power_spin.setSuffix(" dBm"); self.tx_power_spin.setValue(20)
        self.sample_rate_spin = QDoubleSpinBox(); self.sample_rate_spin.setRange(0.1, 1000); self.sample_rate_spin.setSuffix(" Msps"); self.sample_rate_spin.setValue(20); self.sample_rate_spin.setDecimals(1)
        self.modulation_combo = QComboBox()
        self.modulation_combo.addItems(["FHSS", "DSSS", "OFDM", "FSK", "PSK", "QAM", "Unknown"])
        self.protocol_edit = QLineEdit(); self.protocol_edit.setPlaceholderText("Ví dụ: OcuSync 3.0, Lightbridge")
        self.freq_hop_check = QCheckBox("Có nhảy tần (Frequency Hopping)")
        f3.addRow("Tần số trung tâm", self.freq_center_spin)
        f3.addRow("Băng thông", self.freq_bw_spin)
        f3.addRow("Công suất phát", self.tx_power_spin)
        f3.addRow("Tốc độ lấy mẫu", self.sample_rate_spin)
        f3.addRow("SNR (dB)", self.snr_spin)
        f3.addRow("Điều chế", self.modulation_combo)
        f3.addRow("Giao thức", self.protocol_edit)
        f3.addRow("", self.freq_hop_check)
        form_layout.addWidget(g3)

        # ── Notes ──
        g4 = QGroupBox("Ghi chú")
        f4 = QFormLayout(g4)
        self.notes_edit = QTextEdit(); self.notes_edit.setPlaceholderText("Ghi chú thêm về UAV này..."); self.notes_edit.setMaximumHeight(80)
        f4.addRow(self.notes_edit)
        form_layout.addWidget(g4)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        # Buttons
        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Hủy"); btn_cancel.setProperty("class", "secondary")
        btn_save = QPushButton("💾  Lưu UAV"); btn_save.setProperty("class", "success")
        btn_cancel.clicked.connect(self.reject)
        btn_save.clicked.connect(self.accept)
        btn_row.addWidget(btn_cancel)
        btn_row.addStretch()
        btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _populate(self, uav):
        self.name_edit.setText(uav.name)
        self.manufacturer_edit.setText(uav.manufacturer or "")
        self.model_edit.setText(uav.model or "")
        idx = self.category_combo.findText(uav.category or "Consumer")
        if idx >= 0: self.category_combo.setCurrentIndex(idx)
        self.year_spin.setValue(uav.year or 2023)
        self.weight_spin.setValue(uav.weight_g or 0)
        self.max_speed_spin.setValue(uav.max_speed_kmh or 0)
        self.max_altitude_spin.setValue(uav.max_altitude_m or 0)
        self.flight_time_spin.setValue(uav.flight_time_min or 0)
        self.range_spin.setValue(uav.range_km or 0)
        self.battery_spin.setValue(uav.battery_mah or 0)
        self.freq_center_spin.setValue(uav.freq_center_mhz or 2400)
        self.freq_bw_spin.setValue(uav.freq_bandwidth_mhz or 80)
        self.snr_spin.setValue(uav.snr_db or 20)
        self.tx_power_spin.setValue(getattr(uav, 'tx_power_dbm', 20) or 20)
        self.sample_rate_spin.setValue(getattr(uav, 'sample_rate_msps', 20) or 20)
        mod_idx = self.modulation_combo.findText(uav.modulation or "FHSS")
        if mod_idx >= 0: self.modulation_combo.setCurrentIndex(mod_idx)
        self.protocol_edit.setText(uav.protocol or "")
        self.freq_hop_check.setChecked(uav.freq_hopping or False)
        self.notes_edit.setPlainText(uav.notes or "")

    def get_uav_data(self) -> dict:
        return {
            "name": self.name_edit.text().strip(),
            "manufacturer": self.manufacturer_edit.text().strip(),
            "model": self.model_edit.text().strip(),
            "category": self.category_combo.currentText(),
            "year": self.year_spin.value(),
            "weight_g": self.weight_spin.value(),
            "max_speed_kmh": self.max_speed_spin.value(),
            "max_altitude_m": self.max_altitude_spin.value(),
            "flight_time_min": self.flight_time_spin.value(),
            "range_km": self.range_spin.value(),
            "battery_mah": self.battery_spin.value(),
            "freq_center_mhz": self.freq_center_spin.value(),
            "freq_bandwidth_mhz": self.freq_bw_spin.value(),
            "snr_db": self.snr_spin.value(),
            "tx_power_dbm": self.tx_power_spin.value(),
            "sample_rate_msps": self.sample_rate_spin.value(),
            "modulation": self.modulation_combo.currentText(),
            "protocol": self.protocol_edit.text().strip(),
            "freq_hopping": self.freq_hop_check.isChecked(),
            "notes": self.notes_edit.toPlainText().strip(),
        }


# ─────────────────────────── Detail Panel ────────────────────────────
class DetailPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.current_uav = None

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # ── Tab 1: Overview ──
        overview = QWidget()
        ov_layout = QVBoxLayout(overview)
        ov_layout.setContentsMargins(16, 16, 16, 16)
        ov_layout.setSpacing(12)

        self.uav_name_label = QLabel("—")
        self.uav_name_label.setObjectName("title")
        self.uav_name_label.setFont(QFont("Segoe UI", 17, QFont.Weight.Bold))
        self.uav_name_label.setWordWrap(True)
        ov_layout.addWidget(self.uav_name_label)

        self.uav_meta_label = QLabel("—")
        self.uav_meta_label.setObjectName("subtitle")
        ov_layout.addWidget(self.uav_meta_label)

        divider = QFrame(); divider.setObjectName("divider"); divider.setFrameShape(QFrame.Shape.HLine)
        ov_layout.addWidget(divider)

        # Stat cards
        stats_row = QHBoxLayout(); stats_row.setSpacing(10)
        self.stat_cards = {}
        for key, label in [("flight_time", "Thời gian bay"), ("max_speed", "Tốc độ max"), ("range", "Tầm xa"), ("weight", "Trọng lượng")]:
            card = QFrame(); card.setObjectName("stat_card")
            cl = QVBoxLayout(card); cl.setSpacing(4); cl.setContentsMargins(14, 12, 14, 12)
            val = QLabel("—"); val.setObjectName("stat_value"); val.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl = QLabel(label); lbl.setObjectName("stat_label"); lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cl.addWidget(val); cl.addWidget(lbl)
            self.stat_cards[key] = val
            stats_row.addWidget(card)
        ov_layout.addLayout(stats_row)

        # Technical specs table
        specs_group = QGroupBox("Thông số kỹ thuật")
        specs_layout = QVBoxLayout(specs_group); specs_layout.setContentsMargins(8, 8, 8, 8)
        self.specs_table = QTableWidget(0, 2)
        self.specs_table.setHorizontalHeaderLabels(["Thông số", "Giá trị"])
        self.specs_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.specs_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.specs_table.verticalHeader().setVisible(False)
        self.specs_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.specs_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.specs_table.setMaximumHeight(220)
        specs_layout.addWidget(self.specs_table)
        ov_layout.addWidget(specs_group)

        # RF specs
        rf_group = QGroupBox("Thông số RF")
        rf_layout = QVBoxLayout(rf_group); rf_layout.setContentsMargins(8, 8, 8, 8)
        self.rf_table = QTableWidget(0, 2)
        self.rf_table.setHorizontalHeaderLabels(["Thông số", "Giá trị"])
        self.rf_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.rf_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.rf_table.verticalHeader().setVisible(False)
        self.rf_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.rf_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.rf_table.setMaximumHeight(220)
        rf_layout.addWidget(self.rf_table)
        ov_layout.addWidget(rf_group)

        self.notes_label = QLabel("")
        self.notes_label.setWordWrap(True)
        self.notes_label.setStyleSheet("color: #6080a0; font-style: italic; padding: 4px;")
        ov_layout.addWidget(self.notes_label)
        ov_layout.addStretch()

        self.tabs.addTab(overview, "📋  Chi tiết")

        # ── Tab 2: RF Chart ──
        rf_tab = QWidget()
        rf_layout2 = QVBoxLayout(rf_tab)
        rf_layout2.setContentsMargins(8, 8, 8, 8)
        self.rf_chart = RFChartWidget()
        rf_layout2.addWidget(self.rf_chart)
        self.tabs.addTab(rf_tab, "📡  Biểu đồ RF")

    def show_uav(self, uav: 'UAV'):
        self.current_uav = uav
        self.uav_name_label.setText(uav.name)
        meta_parts = []
        if uav.manufacturer: meta_parts.append(uav.manufacturer)
        if uav.model: meta_parts.append(uav.model)
        if uav.year: meta_parts.append(str(uav.year))
        if uav.category: meta_parts.append(f"[{uav.category}]")
        self.uav_meta_label.setText("  ·  ".join(meta_parts) or "Không có thông tin")

        self.stat_cards["flight_time"].setText(f"{uav.flight_time_min or 0} min")
        self.stat_cards["max_speed"].setText(f"{uav.max_speed_kmh or 0} km/h")
        self.stat_cards["range"].setText(f"{uav.range_km or 0} km")
        self.stat_cards["weight"].setText(f"{uav.weight_g or 0} g")

        specs = [
            ("Trọng lượng", f"{uav.weight_g or '—'} g"),
            ("Tốc độ tối đa", f"{uav.max_speed_kmh or '—'} km/h"),
            ("Độ cao tối đa", f"{uav.max_altitude_m or '—'} m"),
            ("Thời gian bay", f"{uav.flight_time_min or '—'} phút"),
            ("Tầm hoạt động", f"{uav.range_km or '—'} km"),
            ("Dung lượng pin", f"{uav.battery_mah or '—'} mAh"),
        ]
        self._fill_table(self.specs_table, specs)

        rf_specs = [
            ("Tần số trung tâm", f"{uav.freq_center_mhz or '—'} MHz"),
            ("Băng thông", f"{uav.freq_bandwidth_mhz or '—'} MHz"),
            ("Công suất phát", f"{getattr(uav, 'tx_power_dbm', '—')} dBm"),
            ("Tốc độ lấy mẫu", f"{getattr(uav, 'sample_rate_msps', '—')} Msps"),
            ("SNR", f"{uav.snr_db or '—'} dB"),
            ("Điều chế", uav.modulation or "—"),
            ("Giao thức", uav.protocol or "—"),
            ("Nhảy tần (FHSS)", "Có ✓" if uav.freq_hopping else "Không"),
        ]
        self._fill_table(self.rf_table, rf_specs)

        if uav.notes:
            self.notes_label.setText(f"📝 {uav.notes}")
        else:
            self.notes_label.setText("")

        self.rf_chart.plot_rf(uav)

    def _fill_table(self, table, rows):
        table.setRowCount(len(rows))
        for i, (k, v) in enumerate(rows):
            k_item = QTableWidgetItem(k)
            k_item.setForeground(QColor("#8090a8"))
            v_item = QTableWidgetItem(str(v))
            v_item.setForeground(QColor("#e0e0e0"))
            table.setItem(i, 0, k_item)
            table.setItem(i, 1, v_item)
            table.setRowHeight(i, 30)

    def clear(self):
        self.current_uav = None
        self.uav_name_label.setText("Chọn UAV từ danh sách")
        self.uav_meta_label.setText("")
        for v in self.stat_cards.values(): v.setText("—")
        self.specs_table.setRowCount(0)
        self.rf_table.setRowCount(0)
        self.notes_label.setText("")
        self.rf_chart._draw_empty()


# ─────────────────────────── Compare Panel ────────────────────────────
class ComparePanel(QWidget):
    def __init__(self, db: 'UAVDatabase', parent=None):
        super().__init__(parent)
        self.db = db
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        header = QLabel("So sánh UAV")
        header.setObjectName("title")
        header.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        layout.addWidget(header)
        layout.addWidget(QLabel("Chọn tối đa 6 UAV để so sánh thông số và phổ RF:"))

        # Selector
        sel_row = QHBoxLayout()
        self.uav_selector = QComboBox()
        self.uav_selector.setMinimumWidth(220)
        btn_add = QPushButton("+ Thêm vào so sánh")
        btn_add.clicked.connect(self._add_uav)
        btn_clear = QPushButton("Xóa tất cả"); btn_clear.setProperty("class", "secondary")
        btn_clear.clicked.connect(self._clear)
        sel_row.addWidget(self.uav_selector)
        sel_row.addWidget(btn_add)
        sel_row.addWidget(btn_clear)
        sel_row.addStretch()
        layout.addLayout(sel_row)

        # Selected tags
        self.tags_row = QHBoxLayout()
        self.tags_row.setSpacing(6)
        layout.addLayout(self.tags_row)

        divider = QFrame(); divider.setObjectName("divider"); divider.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(divider)

        # Comparison table
        self.compare_table = QTableWidget()
        self.compare_table.verticalHeader().setVisible(True)
        self.compare_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.compare_table)

        # Chart
        self.compare_chart = RFChartWidget()
        self.compare_chart.setMinimumHeight(280)
        layout.addWidget(self.compare_chart)

        self.selected_uavs = []
        self.refresh_selector()

    def refresh_selector(self):
        self.uav_selector.clear()
        for u in self.db.get_all():
            self.uav_selector.addItem(u.name, u.id)

    def _add_uav(self):
        if self.uav_selector.count() == 0: return
        uid = self.uav_selector.currentData()
        uav = self.db.get_by_id(uid)
        if uav and uav not in self.selected_uavs and len(self.selected_uavs) < 6:
            self.selected_uavs.append(uav)
            self._refresh_tags()
            self._refresh_table()
            self.compare_chart.plot_comparison(self.selected_uavs)

    def _clear(self):
        self.selected_uavs = []
        self._refresh_tags()
        self._refresh_table()
        self.compare_chart._draw_empty()

    def _remove_uav(self, uav):
        if uav in self.selected_uavs:
            self.selected_uavs.remove(uav)
            self._refresh_tags()
            self._refresh_table()
            if self.selected_uavs:
                self.compare_chart.plot_comparison(self.selected_uavs)
            else:
                self.compare_chart._draw_empty()

    def _refresh_tags(self):
        while self.tags_row.count():
            item = self.tags_row.takeAt(0)
            if item.widget(): item.widget().deleteLater()
        colors = ['#1a3d6e', '#5c1a1a', '#1a5c2e', '#5c4a1a', '#3a1a5c', '#1a4a5c']
        for i, uav in enumerate(self.selected_uavs):
            tag = QPushButton(f"✕  {uav.name}")
            tag.setStyleSheet(f"background-color: {colors[i%len(colors)]}; color: #c0d0ff; border-radius: 12px; padding: 4px 12px; font-size: 12px;")
            uav_ref = uav
            tag.clicked.connect(lambda _, u=uav_ref: self._remove_uav(u))
            self.tags_row.addWidget(tag)
        self.tags_row.addStretch()

    def _refresh_table(self):
        if not self.selected_uavs:
            self.compare_table.setRowCount(0)
            self.compare_table.setColumnCount(0)
            return
        fields = [
            ("Hãng", "manufacturer"), ("Danh mục", "category"), ("Năm", "year"),
            ("Trọng lượng (g)", "weight_g"), ("Tốc độ (km/h)", "max_speed_kmh"),
            ("Độ cao (m)", "max_altitude_m"), ("Bay (phút)", "flight_time_min"),
            ("Tầm xa (km)", "range_km"), ("Pin (mAh)", "battery_mah"),
            ("Tần số (MHz)", "freq_center_mhz"), ("Băng thông (MHz)", "freq_bandwidth_mhz"),
            ("SNR (dB)", "snr_db"), ("Điều chế", "modulation"), ("FHSS", "freq_hopping"),
            ("Công suất (dBm)", "tx_power_dbm"),
            ("Lấy mẫu (Msps)", "sample_rate_msps"),
        ]
        self.compare_table.setRowCount(len(fields))
        self.compare_table.setColumnCount(len(self.selected_uavs))
        self.compare_table.setHorizontalHeaderLabels([u.name for u in self.selected_uavs])
        self.compare_table.setVerticalHeaderLabels([f[0] for f in fields])
        self.compare_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        for ci, uav in enumerate(self.selected_uavs):
            for ri, (label, attr) in enumerate(fields):
                val = getattr(uav, attr, None)
                if isinstance(val, bool):
                    text = "Có ✓" if val else "Không"
                elif val is None or val == 0:
                    text = "—"
                else:
                    text = str(val)
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.compare_table.setItem(ri, ci, item)
                self.compare_table.setRowHeight(ri, 30)


# ─────────────────────────── Main Window ────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = UAVDatabase()
        self.setWindowTitle("🚁  UAV Database — Cơ sở dữ liệu UAV")
        self.setMinimumSize(1280, 780)
        self.setStyleSheet(DARK_STYLE)
        self._build_ui()
        self._load_table()
        self._update_stats()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Top Bar ──
        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: #141720; border-bottom: 1px solid #2e3340;")
        top_bar.setFixedHeight(64)
        tbl = QHBoxLayout(top_bar)
        tbl.setContentsMargins(20, 0, 20, 0)

        icon_label = QLabel("🚁")
        icon_label.setFont(QFont("Segoe UI", 22))
        title_label = QLabel("UAV Database")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #e8f0ff;")
        sub_label = QLabel("Cơ sở dữ liệu UAV & tín hiệu RF")
        sub_label.setStyleSheet("color: #506080; font-size: 12px;")
        sub_col = QVBoxLayout(); sub_col.setSpacing(1)
        sub_col.addWidget(title_label); sub_col.addWidget(sub_label)
        tbl.addWidget(icon_label)
        tbl.addSpacing(10)
        tbl.addLayout(sub_col)
        tbl.addStretch()

        # Stats in topbar
        self.stat_labels = {}
        for key, label in [("total", "UAV"), ("categories", "Danh mục"), ("manufacturers", "Hãng")]:
            s_val = QLabel("0"); s_val.setObjectName("stat_value"); s_val.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
            s_lbl = QLabel(label); s_lbl.setObjectName("stat_label")
            s_col = QVBoxLayout(); s_col.setSpacing(0); s_col.setContentsMargins(16, 0, 16, 0)
            s_col.addWidget(s_val, alignment=Qt.AlignmentFlag.AlignCenter)
            s_col.addWidget(s_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
            self.stat_labels[key] = s_val
            tbl.addLayout(s_col)
        root.addWidget(top_bar)

        # ── Main Content ──
        main_tabs = QTabWidget()
        main_tabs.setTabPosition(QTabWidget.TabPosition.West)
        main_tabs.setStyleSheet("""
            QTabWidget::pane { border: none; }
            QTabBar { background-color: #141720; }
            QTabBar::tab { background-color: #141720; color: #506080; padding: 14px 16px;
                           border: none; border-right: 2px solid transparent;
                           font-size: 13px; font-weight: 500; min-width: 130px; text-align: left; }
            QTabBar::tab:selected { color: #4a9eff; border-right: 2px solid #4a9eff; background-color: #1a1d23; }
            QTabBar::tab:hover { color: #c0d0e8; background-color: #1e2230; }
        """)
        root.addWidget(main_tabs)

        # ── Tab: Danh sách ──
        list_tab = QWidget()
        list_layout = QVBoxLayout(list_tab)
        list_layout.setContentsMargins(16, 16, 16, 16)
        list_layout.setSpacing(10)

        # Toolbar
        toolbar = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍  Tìm kiếm theo tên, hãng, model...")
        self.search_box.setFixedHeight(36)
        self.search_box.textChanged.connect(self._filter_table)
        self.cat_filter = QComboBox()
        self.cat_filter.setFixedHeight(36); self.cat_filter.setMinimumWidth(140)
        self.cat_filter.addItem("Tất cả danh mục")
        self.cat_filter.addItems(["Consumer", "Professional", "Military", "Racing", "Agricultural", "Research", "Industrial"])
        self.cat_filter.currentTextChanged.connect(self._filter_table)

        btn_add = QPushButton("＋  Thêm UAV"); btn_add.setFixedHeight(36)
        btn_add.clicked.connect(self._add_uav)
        btn_edit = QPushButton("✏️  Sửa"); btn_edit.setFixedHeight(36); btn_edit.setProperty("class", "secondary")
        btn_edit.clicked.connect(self._edit_uav)
        btn_del = QPushButton("🗑  Xóa"); btn_del.setFixedHeight(36); btn_del.setProperty("class", "danger")
        btn_del.clicked.connect(self._delete_uav)
        self.btn_edit = btn_edit; self.btn_del = btn_del

        toolbar.addWidget(self.search_box, stretch=3)
        toolbar.addWidget(self.cat_filter)
        toolbar.addStretch()
        toolbar.addWidget(btn_add)
        toolbar.addWidget(btn_edit)
        toolbar.addWidget(btn_del)
        list_layout.addLayout(toolbar)

        # Splitter: table | detail
        splitter = QSplitter(Qt.Orientation.Horizontal)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Tên UAV", "Hãng", "Danh mục", "Tần số (MHz)", "Bay (phút)", "SNR (dB)", "Năm"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for c in range(1, 7):
            self.table.horizontalHeader().setSectionResizeMode(c, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.itemSelectionChanged.connect(self._on_selection)
        self.table.doubleClicked.connect(self._edit_uav)
        splitter.addWidget(self.table)

        self.detail_panel = DetailPanel()
        splitter.addWidget(self.detail_panel)
        splitter.setSizes([700, 500])

        list_layout.addWidget(splitter)
        main_tabs.addTab(list_tab, "📋  Danh sách")

        # ── Tab: So sánh ──
        self.compare_panel = ComparePanel(self.db)
        main_tabs.addTab(self.compare_panel, "⚖️  So sánh")

        main_tabs.currentChanged.connect(self._on_tab_changed)
        self.main_tabs = main_tabs

    def _on_tab_changed(self, idx):
        if idx == 1:
            self.compare_panel.refresh_selector()

    def _load_table(self, uavs=None):
        if uavs is None:
            uavs = self.db.get_all()
        self.table.setRowCount(len(uavs))
        self._displayed_uavs = uavs
        for row, uav in enumerate(uavs):
            items = [
                uav.name,
                uav.manufacturer or "—",
                uav.category or "—",
                str(uav.freq_center_mhz or "—"),
                str(uav.flight_time_min or "—"),
                str(uav.snr_db or "—"),
                str(uav.year or "—"),
            ]
            for col, text in enumerate(items):
                item = QTableWidgetItem(text)
                item.setData(Qt.ItemDataRole.UserRole, uav.id)
                if col == 0:
                    item.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
                    item.setForeground(QColor("#c8deff"))
                self.table.setItem(row, col, item)
            self.table.setRowHeight(row, 36)
        self.detail_panel.clear()

    def _filter_table(self):
        query = self.search_box.text().lower().strip()
        cat = self.cat_filter.currentText()
        all_uavs = self.db.get_all()
        filtered = []
        for u in all_uavs:
            if cat != "Tất cả danh mục" and u.category != cat:
                continue
            if query:
                searchable = f"{u.name} {u.manufacturer or ''} {u.model or ''} {u.protocol or ''}".lower()
                if query not in searchable:
                    continue
            filtered.append(u)
        self._load_table(filtered)
        self._update_stats()

    def _on_selection(self):
        selected = self.table.selectedItems()
        if not selected:
            self.detail_panel.clear()
            return
        uid = self.table.item(self.table.currentRow(), 0).data(Qt.ItemDataRole.UserRole)
        uav = self.db.get_by_id(uid)
        if uav:
            self.detail_panel.show_uav(uav)

    def _add_uav(self):
        dlg = UAVFormDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_uav_data()
            if not data["name"]:
                QMessageBox.warning(self, "Lỗi", "Tên UAV không được để trống!")
                return
            uav = UAV(**data)
            self.db.add(uav)
            self._load_table()
            self._update_stats()

    def _edit_uav(self):
        if self.table.currentRow() < 0: return
        uid = self.table.item(self.table.currentRow(), 0).data(Qt.ItemDataRole.UserRole)
        uav = self.db.get_by_id(uid)
        if not uav: return
        dlg = UAVFormDialog(self, uav)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_uav_data()
            if not data["name"]:
                QMessageBox.warning(self, "Lỗi", "Tên UAV không được để trống!")
                return
            for k, v in data.items():
                setattr(uav, k, v)
            self.db.save()
            self._load_table()
            self._update_stats()

    def _delete_uav(self):
        if self.table.currentRow() < 0: return
        uid = self.table.item(self.table.currentRow(), 0).data(Qt.ItemDataRole.UserRole)
        uav = self.db.get_by_id(uid)
        if not uav: return
        reply = QMessageBox.question(self, "Xác nhận xóa",
            f"Bạn có chắc muốn xóa UAV:\n\n«{uav.name}»?\n\nHành động này không thể hoàn tác.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete(uid)
            self._load_table()
            self._update_stats()
            self.detail_panel.clear()

    def _update_stats(self):
        all_uavs = self.db.get_all()
        self.stat_labels["total"].setText(str(len(all_uavs)))
        cats = len(set(u.category for u in all_uavs if u.category))
        self.stat_labels["categories"].setText(str(cats))
        mans = len(set(u.manufacturer for u in all_uavs if u.manufacturer))
        self.stat_labels["manufacturers"].setText(str(mans))


# ─────────────────────────── Entry Point ────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
