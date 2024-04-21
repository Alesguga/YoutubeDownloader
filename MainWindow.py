from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                               QProgressBar, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt
from pytube import YouTube, exceptions
import sys

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Downloader de videos de YouTube')
        self.setGeometry(300, 300, 500, 350)  # x, y, width, height
        self.setStyleSheet('background-color: #E5EAF0;')

        self.label = QLabel('Descarga tus videos', self)
        self.label.setStyleSheet('font: 20pt "Segoe UI"; margin-top: 20px;color:#1B3A57; ')
        self.label.setAlignment(Qt.AlignCenter)

        self.link_label = QLabel('Pega el link aquí:', self)
        self.link_label.setStyleSheet('font: 14pt "Segoe UI"; color:#1B3A57; margin-top: 10px;')
        self.link_label.setAlignment(Qt.AlignCenter)

        self.link_edit = QLineEdit(self)
        self.link_edit.setStyleSheet('font: 14pt "Segoe UI";color:#1B3A57; padding: 5px;')

        self.download_button = QPushButton('DESCARGAR', self)
        self.download_button.setStyleSheet('font: 14pt "Segoe UI" bold; background-color: #1B3A57; color: white; padding: 5px; border-radius: 10px;')
        self.download_button.clicked.connect(self.downloader)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet('height: 20px; border-radius: 10px;')
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setMaximum(100)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.link_label)
        self.layout.addWidget(self.link_edit)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.progress_bar)
        self.layout.setSpacing(10)

    def downloader(self):
        try:
            video_url = self.link_edit.text()
            yt = YouTube(video_url, on_progress_callback=self.progress_callback)
            video = yt.streams.get_highest_resolution()
            save_path = QFileDialog.getExistingDirectory(self, "Select Download Folder")
            if save_path:
                video.download(save_path)
                self.label.setText('¡Descarga completada!')
                self.progress_bar.setValue(100)
        except exceptions.PytubeError as e:
            QMessageBox.critical(self, "Error", f"Failed to download video: {e}")
            self.progress_bar.setValue(0)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")
            self.progress_bar.setValue(0)

    def progress_callback(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = int(bytes_downloaded / total_size * 100)
        self.progress_bar.setValue(percentage)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())
