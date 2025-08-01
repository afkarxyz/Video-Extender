import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, 
                             QMessageBox, QTextEdit, QListWidget, QMenu,
                             QTabWidget, QSpinBox, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt6.QtGui import QTextCursor, QIcon, QDragEnterEvent, QDropEvent, QPainter, QAction

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    
    return os.path.join(base_path, relative_path)

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        ffmpeg_path = get_resource_path('ffmpeg.exe')
        ffprobe_path = get_resource_path('ffprobe.exe')
    else:
        ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')
        ffprobe_path = os.path.join(os.path.dirname(__file__), 'ffprobe.exe')
    
    return ffmpeg_path, ffprobe_path

FFMPEG_PATH, FFPROBE_PATH = get_ffmpeg_path()

class DragDropListWidget(QListWidget):
    files_dropped = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.original_style = self.styleSheet()
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v', 
                               '.mpg', '.mpeg', '.m2v', '.m2ts', '.mts', '.ts', '.vob', '.3gp',
                               '.3g2', '.f4v', '.asf', '.rmvb', '.rm', '.ogv', '.mxf', '.dv',
                               '.divx', '.xvid', '.mpv', '.m2p', '.mp2', '.mpeg2', '.ogm'}
            has_video = False
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if any(file_path.lower().endswith(ext) for ext in video_extensions):
                        has_video = True
                        break
            
            if has_video:
                self.setStyleSheet(self.original_style + """
                    QListWidget {
                        border: 2px dashed #4CAF50;
                        background-color: #E8F5E8;
                    }
                """)
                event.acceptProposedAction()
            else:
                self.setStyleSheet(self.original_style + """
                    QListWidget {
                        border: 2px dashed #F44336;
                        background-color: #FFEBEE;
                    }
                """)
                event.ignore()
        else:
            event.ignore()
        
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v', 
                               '.mpg', '.mpeg', '.m2v', '.m2ts', '.mts', '.ts', '.vob', '.3gp',
                               '.3g2', '.f4v', '.asf', '.rmvb', '.rm', '.ogv', '.mxf', '.dv',
                               '.divx', '.xvid', '.mpv', '.m2p', '.mp2', '.mpeg2', '.ogm'}
            has_video = False
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if any(file_path.lower().endswith(ext) for ext in video_extensions):
                        has_video = True
                        break
            
            if has_video:
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        self.setStyleSheet(self.original_style)
        super().dragLeaveEvent(event)
            
    def dropEvent(self, event: QDropEvent):
        self.setStyleSheet(self.original_style)
        
        if event.mimeData().hasUrls():
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v', 
                               '.mpg', '.mpeg', '.m2v', '.m2ts', '.mts', '.ts', '.vob', '.3gp',
                               '.3g2', '.f4v', '.asf', '.rmvb', '.rm', '.ogv', '.mxf', '.dv',
                               '.divx', '.xvid', '.mpv', '.m2p', '.mp2', '.mpeg2', '.ogm'}
            video_files = []
            
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if any(file_path.lower().endswith(ext) for ext in video_extensions):
                        video_files.append(file_path)
            
            if video_files:
                self.files_dropped.emit(video_files)
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.count() == 0:
            painter = QPainter(self.viewport())
            painter.save()
            col = self.palette().placeholderText().color()
            painter.setPen(col)
            fm = self.fontMetrics()
            elided_text = fm.elidedText(
                "📁 Drag & drop video files here or click 'Add Files'", 
                Qt.TextElideMode.ElideRight, 
                self.viewport().width()
            )
            painter.drawText(self.viewport().rect(), Qt.AlignmentFlag.AlignCenter, elided_text)
            painter.restore()

class DragDropTextEdit(QTextEdit):
    file_dropped = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.original_style = self.styleSheet()
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v', 
                               '.mpg', '.mpeg', '.m2v', '.m2ts', '.mts', '.ts', '.vob', '.3gp',
                               '.3g2', '.f4v', '.asf', '.rmvb', '.rm', '.ogv', '.mxf', '.dv',
                               '.divx', '.xvid', '.mpv', '.m2p', '.mp2', '.mpeg2', '.ogm'}
            has_video = False
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if any(file_path.lower().endswith(ext) for ext in video_extensions):
                        has_video = True
                        break
            
            if has_video:
                self.setStyleSheet(self.original_style + """
                    QTextEdit {
                        border: 2px dashed #4CAF50;
                        background-color: #E8F5E8;
                    }
                """)
                event.acceptProposedAction()
            else:
                self.setStyleSheet(self.original_style + """
                    QTextEdit {
                        border: 2px dashed #F44336;
                        background-color: #FFEBEE;
                    }
                """)
                event.ignore()
        else:
            event.ignore()
        
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v', 
                               '.mpg', '.mpeg', '.m2v', '.m2ts', '.mts', '.ts', '.vob', '.3gp',
                               '.3g2', '.f4v', '.asf', '.rmvb', '.rm', '.ogv', '.mxf', '.dv',
                               '.divx', '.xvid', '.mpv', '.m2p', '.mp2', '.mpeg2', '.ogm'}
            has_video = False
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if any(file_path.lower().endswith(ext) for ext in video_extensions):
                        has_video = True
                        break
            
            if has_video:
                event.acceptProposedAction()
            else:
                event.ignore()
        else:
            event.ignore()
    
    def dragLeaveEvent(self, event):
        self.setStyleSheet(self.original_style)
        super().dragLeaveEvent(event)
            
    def dropEvent(self, event: QDropEvent):
        self.setStyleSheet(self.original_style)
        
        if event.mimeData().hasUrls():
            video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v', 
                               '.mpg', '.mpeg', '.m2v', '.m2ts', '.mts', '.ts', '.vob', '.3gp',
                               '.3g2', '.f4v', '.asf', '.rmvb', '.rm', '.ogv', '.mxf', '.dv',
                               '.divx', '.xvid', '.mpv', '.m2p', '.mp2', '.mpeg2', '.ogm'}
            
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    file_path = url.toLocalFile()
                    if any(file_path.lower().endswith(ext) for ext in video_extensions):
                        self.file_dropped.emit(file_path)
                        event.acceptProposedAction()
                        return
            
            event.ignore()
        else:
            event.ignore()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.toPlainText().strip():
            painter = QPainter(self.viewport())
            painter.save()
            col = self.palette().placeholderText().color()
            painter.setPen(col)
            fm = self.fontMetrics()
            elided_text = fm.elidedText(
                "📁 Drag & drop video file here or click 'Add File'", 
                Qt.TextElideMode.ElideRight, 
                self.viewport().width()
            )
            painter.drawText(self.viewport().rect(), Qt.AlignmentFlag.AlignCenter, elided_text)
            painter.restore()
            
class VideoExtenderWorker(QThread):
    progress = pyqtSignal(str)
    progress_percent = pyqtSignal(int)
    file_progress = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, input_files, hours, minutes, times):
        super().__init__()
        self.input_files = input_files
        self.hours = hours
        self.minutes = minutes
        self.times = times
        self.total_duration = 0
        self.is_running = True

    def parse_ffmpeg_progress(self, line):
        if 'time=' in line and self.total_duration > 0:
            try:
                time_part = line.split('time=')[1].split()[0]
                time_parts = time_part.split(':')
                if len(time_parts) == 3:
                    hours = float(time_parts[0])
                    minutes = float(time_parts[1])
                    seconds = float(time_parts[2])
                    current_seconds = hours * 3600 + minutes * 60 + seconds
                    progress = min(int((current_seconds / self.total_duration) * 100), 100)
                    self.progress_percent.emit(progress)
            except:
                pass

    def run(self):
        total_files = len(self.input_files)
        
        for i, input_file in enumerate(self.input_files):
            if not self.is_running:
                break
                
            try:
                from subprocess import CREATE_NO_WINDOW
                
                self.status_updated.emit(f"Processing: {os.path.basename(input_file)}")
                
                duration_cmd = [
                    FFPROBE_PATH, '-v', 'error',
                    '-show_entries', 'format=duration',
                    '-of', 'default=noprint_wrappers=1:nokey=1',
                    input_file
                ]
                
                duration = float(subprocess.check_output(
                    duration_cmd,
                    creationflags=CREATE_NO_WINDOW
                ).decode().strip())
                
                if self.times > 0:
                    repeat = self.times
                else:
                    desired_seconds = (self.hours * 3600) + (self.minutes * 60)
                    repeat = int((desired_seconds + duration - 1) / duration)
                
                self.total_duration = duration * repeat
                
                concat_file = "concat.txt"
                with open(concat_file, 'w') as f:
                    for _ in range(repeat):
                        f.write(f"file '{input_file}'\n")
                
                name, ext = os.path.splitext(input_file)
                if self.times > 0:
                    output_file = f"{name}_{self.times}times{ext}"
                else:
                    time_str = f"{self.hours}h{self.minutes}m" if self.minutes > 0 else f"{self.hours}h"
                    output_file = f"{name}_{time_str}{ext}"
                
                ffmpeg_cmd = [
                    FFMPEG_PATH,
                    '-f', 'concat',
                    '-safe', '0',
                    '-i', concat_file,
                    '-c', 'copy',
                    '-progress', 'pipe:2',
                    output_file
                ]
                
                process = subprocess.Popen(
                    ffmpeg_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    creationflags=CREATE_NO_WINDOW
                )
                
                while True:
                    if not self.is_running:
                        process.terminate()
                        break
                        
                    line = process.stderr.readline()
                    if not line:
                        break
                    line = line.strip()
                    if line:
                        self.parse_ffmpeg_progress(line)
                
                process.wait()
                os.remove(concat_file)
                
                if process.returncode == 0:
                    self.status_updated.emit(f"✅ Completed: {os.path.basename(input_file)}")
                    self.progress_percent.emit(100)
                else:
                    self.status_updated.emit(f"❌ Failed: {os.path.basename(input_file)}")
                
                progress = int((i + 1) / total_files * 100)
                self.file_progress.emit(progress)
                
            except Exception as e:
                self.status_updated.emit(f"❌ Error: {str(e)}")
        
        if self.is_running:
            self.finished.emit(True, "All videos processed successfully!")
        else:
            self.finished.emit(False, "Processing cancelled")
    
    def stop(self):
        self.is_running = False

class VideoExtender(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('videoextender', 'Video Extender')
        self.input_files = []
        self.initUI()
        
        self.setWindowTitle('Video Extender')
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def normalize_path(self, path):
        if not path:
            return path
            
        normalized_path = os.path.normpath(path)
        
        if len(normalized_path) >= 2 and normalized_path[1] == ':':
            normalized_path = normalized_path[0].upper() + normalized_path[1:]
        
        return normalized_path

    def initUI(self):
        self.setWindowTitle('Video Extender')
        self.setFixedSize(400, 330)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(5)

        hours_label = QLabel('Hours:')
        self.hours_input = QSpinBox()
        self.hours_input.setMaximumWidth(60)
        self.hours_input.setRange(0, 1000)
        self.hours_input.setValue(1)
        settings_layout.addWidget(hours_label)
        settings_layout.addWidget(self.hours_input)

        minutes_label = QLabel('Minutes:')
        self.minutes_input = QSpinBox()
        self.minutes_input.setMaximumWidth(60)
        self.minutes_input.setRange(0, 59)
        self.minutes_input.setValue(0)
        settings_layout.addWidget(minutes_label)
        settings_layout.addWidget(self.minutes_input)

        times_label = QLabel('Times:')
        self.times_input = QSpinBox()
        self.times_input.setMaximumWidth(60)
        self.times_input.setRange(0, 1000)
        self.times_input.setValue(0)
        settings_layout.addWidget(times_label)
        settings_layout.addWidget(self.times_input)
        
        settings_layout.addStretch()

        self.times_input.valueChanged.connect(self.on_times_changed)
        self.hours_input.valueChanged.connect(self.on_duration_changed)
        self.minutes_input.valueChanged.connect(self.on_duration_changed)

        main_layout.addLayout(settings_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        self.create_file_selection_tab()
        self.create_progress_tab()
        self.create_about_tab()
        
        self.setLayout(main_layout)

    def create_file_selection_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(5)
        
        button_layout = QHBoxLayout()
        self.add_files_btn = QPushButton("Add Files")
        self.add_files_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_files_btn.clicked.connect(self.add_files)
        self.clear_files_btn = QPushButton("Clear All")
        self.clear_files_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_files_btn.clicked.connect(self.clear_files)
        
        button_layout.addWidget(self.add_files_btn)
        button_layout.addWidget(self.clear_files_btn)
        layout.addLayout(button_layout)
        
        self.file_list = DragDropListWidget()
        self.file_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self.show_context_menu)
        self.file_list.files_dropped.connect(self.handle_dropped_files)
        layout.addWidget(self.file_list)
        
        control_layout = QHBoxLayout()
        
        self.process_btn = QPushButton('Start Processing')
        self.process_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.process_btn.setFixedWidth(150)
        self.process_btn.clicked.connect(self.process_videos)
        control_layout.addWidget(self.process_btn)
        
        layout.addLayout(control_layout)
        
        self.tab_widget.addTab(tab, "File Selection")

    def create_progress_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(5)
        
        self.file_progress_label = QLabel("File Progress:")
        self.file_progress_label.setVisible(False)
        layout.addWidget(self.file_progress_label)
        
        self.file_progress_bar = QProgressBar()
        self.file_progress_bar.setVisible(False)
        layout.addWidget(self.file_progress_bar)
        
        self.ffmpeg_progress_label = QLabel("Current File Progress:")
        self.ffmpeg_progress_label.setVisible(False)
        layout.addWidget(self.ffmpeg_progress_label)
        
        self.ffmpeg_progress_bar = QProgressBar()
        self.ffmpeg_progress_bar.setVisible(False)
        layout.addWidget(self.ffmpeg_progress_bar)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
        
        stop_layout = QHBoxLayout()
        stop_layout.addStretch()
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_btn.setFixedWidth(150)
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        stop_layout.addWidget(self.stop_btn)
        
        stop_layout.addStretch()
        layout.addLayout(stop_layout)
        
        self.tab_widget.addTab(tab, "Progress")

    def create_about_tab(self):

        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        icon_svg_path = get_resource_path("icon.png")
        if os.path.exists(icon_svg_path):
            icon_label = QLabel()
            pixmap = QIcon(icon_svg_path).pixmap(64, 64)
            icon_label.setPixmap(pixmap)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(icon_label)

        about_text = QLabel("""
<h3>Video Extender</h3>
<p><b>Version:</b> 1.0</p>

<p><b>Supported Input Formats:</b><br>
MP4, AVI, MOV, MKV, WMV, FLV, WEBM, M4V, MPG, MPEG, M2V, M2TS, MTS, TS, VOB, 3GP, 3G2, F4V, ASF, RMVB, RM, OGV, MXF, DV, DIVX, XVID, MPV, M2P, MP2, MPEG2, OGM</p>

<p><b>GitHub:</b><br>
<a href="https://github.com/afkarxyz/Video-Extender">https://github.com/afkarxyz/Video-Extender</a></p>
        """)
        about_text.setWordWrap(True)
        about_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        about_text.setOpenExternalLinks(True)
        layout.addWidget(about_text)

        layout.addStretch()
        
        self.tab_widget.addTab(tab, "About")

    def on_times_changed(self, value):
        if value > 0:
            self.hours_input.setValue(0)
            self.minutes_input.setValue(0)
            self.hours_input.setEnabled(False)
            self.minutes_input.setEnabled(False)
        else:
            self.hours_input.setEnabled(True)
            self.minutes_input.setEnabled(True)

    def on_duration_changed(self, value):
        if self.hours_input.value() > 0 or self.minutes_input.value() > 0:
            self.times_input.setValue(0)

    def add_files(self):
        video_formats = "Video Files ("
        extensions = [
            "*.mp4", "*.avi", "*.mov", "*.mkv", "*.wmv", "*.flv", "*.webm", 
            "*.m4v", "*.mpg", "*.mpeg", "*.m2v", "*.m2ts", "*.mts", "*.ts", 
            "*.vob", "*.3gp", "*.3g2", "*.f4v", "*.asf", "*.rmvb", "*.rm", 
            "*.ogv", "*.mxf", "*.dv", "*.divx", "*.xvid", "*.mpv", "*.m2p", 
            "*.mp2", "*.mpeg2", "*.ogm"
        ]
        video_formats += " ".join(extensions) + ")"
        
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Video Files",
            "",
            video_formats
        )
        
        if files:
            for file in files:
                if file not in self.input_files:
                    self.input_files.append(file)
                    self.file_list.addItem(os.path.basename(file))                    
            pass
    
    def handle_dropped_files(self, files):
        added_count = 0
        for file in files:
            if file not in self.input_files:
                self.input_files.append(file)
                self.file_list.addItem(os.path.basename(file))
                added_count += 1
        
    def clear_files(self):
        self.input_files.clear()
        self.file_list.clear()
    
    def show_context_menu(self, position):
        item = self.file_list.itemAt(position)
        if item is not None:
            context_menu = QMenu(self)
            delete_action = QAction("Delete", self)
            delete_action.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_TrashIcon))
            delete_action.triggered.connect(self.delete_selected_file)
            context_menu.addAction(delete_action)
            context_menu.exec(self.file_list.mapToGlobal(position))
    
    def delete_selected_file(self):
        current_row = self.file_list.currentRow()
        if current_row >= 0:
            item = self.file_list.takeItem(current_row)
            if current_row < len(self.input_files):
                removed_file = self.input_files.pop(current_row)

    def process_videos(self):
        if not self.input_files:
            QMessageBox.warning(self, 'Warning', 'Please add video files first!')
            return

        if not os.path.exists(FFMPEG_PATH) or not os.path.exists(FFPROBE_PATH):
            QMessageBox.warning(self, 'Warning', 'FFmpeg files not found. Please ensure ffmpeg.exe and ffprobe.exe are in the same directory as this application.')
            return

        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        times = self.times_input.value()
        
        self.tab_widget.setCurrentIndex(1)
        
        self.worker = VideoExtenderWorker(self.input_files, hours, minutes, times)
        self.worker.progress.connect(self.update_log)
        self.worker.progress_percent.connect(self.update_ffmpeg_progress)
        self.worker.file_progress.connect(self.update_file_progress)
        self.worker.status_updated.connect(self.update_status)
        self.worker.finished.connect(self.on_process_finished)
        
        self.process_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        if len(self.input_files) == 1:
            self.file_progress_label.setVisible(False)
            self.file_progress_bar.setVisible(False)
            self.ffmpeg_progress_label.setVisible(True)
            self.ffmpeg_progress_bar.setVisible(True)
            self.ffmpeg_progress_bar.setValue(0)
        else:
            self.file_progress_label.setVisible(True)
            self.file_progress_bar.setVisible(True)
            self.file_progress_bar.setValue(0)
            self.ffmpeg_progress_label.setVisible(True)
            self.ffmpeg_progress_bar.setVisible(True)
            self.ffmpeg_progress_bar.setValue(0)
        
        self.log_text.clear()
        self.log_text.append(f"Starting processing of {len(self.input_files)} file(s)")
        if len(self.input_files) > 1:
            self.log_text.append(f"Hours: {hours}, Minutes: {minutes}, Times: {times}")
        self.log_text.append("-" * 50)
        self.worker.start()

    def stop_processing(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
            self.log_text.append("\nProcessing stopped by user")
            self.process_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.file_progress_bar.setVisible(False)
            self.ffmpeg_progress_bar.setVisible(False)
            self.file_progress_label.setVisible(False)
            self.ffmpeg_progress_label.setVisible(False)

    def update_log(self, message):
        if any(keyword in message.lower() for keyword in ['error', 'warning', 'failed', 'success', 'completed']):
            self.log_text.append(message)
            self.log_text.moveCursor(QTextCursor.MoveOperation.End)

    def update_ffmpeg_progress(self, percent):
        self.ffmpeg_progress_bar.setValue(percent)

    def update_file_progress(self, percent):
        self.file_progress_bar.setValue(percent)

    def update_status(self, message):
        self.log_text.append(message)
        self.log_text.moveCursor(QTextCursor.MoveOperation.End)

    def on_process_finished(self, success, message):
        self.process_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.file_progress_bar.setVisible(False)
        self.ffmpeg_progress_bar.setVisible(False)
        self.file_progress_label.setVisible(False)
        self.ffmpeg_progress_label.setVisible(False)

        if success:
            self.log_text.append(f"\n{message}")
        else:
            self.log_text.append(f"\nError: {message}")
            QMessageBox.critical(self, 'Error', f'An error occurred: {message}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = VideoExtender()
    ex.show()
    sys.exit(app.exec())