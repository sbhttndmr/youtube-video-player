import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QUrl, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView
from tkinter import filedialog
from tkinter import messagebox
import tkinter
import os
from pytube import YouTube


__version__ = "v1.0"
__author__ = "sabo"

class YouTubePlayer(QWidget):
    def __init__(self, video_id, parent=None):
        super().__init__()
        self.parent = parent
        self.video_id = video_id

        defaultSettings = QWebEngineSettings.globalSettings()
        defaultSettings.setFontSize(QWebEngineSettings.MinimumFontSize, 25)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        topLayout = QHBoxLayout()
        self.layout.addLayout(topLayout)

        label = QLabel("Video ID: ")
        self.input = QLineEdit()
        self.input.installEventFilter(self)
        self.input.setText(self.video_id)

        topLayout.addWidget(label, 1)
        topLayout.addWidget(self.input, 9)

        self.addWebView(self.input.text())

        buttonLayout = QHBoxLayout()
        self.layout.addLayout(buttonLayout)

        buttonUpdate = QPushButton("Show", clicked=self.updateVideo)
        buttonRemove = QPushButton("Delete", clicked=self.removePlayer)
        #buttonDownload = QPushButton("İndir", clicked=DownloadScreen.download)
        buttonLayout.addWidget(buttonUpdate)
        buttonLayout.addWidget(buttonRemove)
        #buttonLayout.addWidget(buttonDownload)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                self.updateVideo()
        return super().eventFilter(source, event)
        
    def addWebView(self, video_id):
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl(f"https://www.youtube.com/embed/" + self.video_id))
        self.layout.addWidget(self.webview)

    def updateVideo(self):
        video_Id = self.input.text()
        self.webview.setUrl(QUrl(f"https://www.youtube.com/embed/" + video_Id))

    def removePlayer(self):
        widget = self.sender().parent()
        widget.setParent(None)
        widget.deleteLater()

        self.organizeLayout()

    def organizeLayout(self):
        playerCount = self.parent.videoGrid.count()
        players = []

        for i in reversed(range(playerCount)):
            widget = self.parent.videoGrid.itemAt(i).widget()
            player.append(widget)
        
        for indx, player in enumerate(players[::-1]):
            self.parent.videoGrid.addWidget(player, indx % 3, indx // 3)

class DownloadScreen(QWidget):
    def __init__(self):
        self.setWindowTitle("Dosya İndirme")
        self.setMinimumSize(750,250)
        downloadwindow = DownloadScreen()
        downloadwindow.show()

    def download(self):
        self.link = ("https://www.youtube.com/v/" + self.video_Id)
        self.currdir = os.getcwd()
        self.savedir = filedialog.askdirectory(parent=window, initialdir=self.currdir, title='Please select a directory')
        if len(self.savedir) > 0:
            return self.savedir
        self.file_path = self.savedir
        
        try:
            self.yt = YouTube(self.link)
        except:
            messagebox.showerror("Hata", "Video bulunamadı")
        
        self.mp4files = self.yt.filter('mp4')
        self.yt.set_filename("video")
        self.d_video = self.yt.get(self.mp4files[-1].extension,self.mp4files[-1].resolution)
        try:
            self.d_video.download(self.file_path)
        except:
            messagebox.showerror("Hata", "Video indirilemedi")
        messagebox.showinfo("Bilgi","Video başarıyla indirildi")

class Youtubewindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Video Player")
        self.setWindowIcon(QIcon("yt.ico"))
        self.setMinimumSize(1400,750)
        self.players = []

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        buttonAddPlayer = QPushButton("&Add Player", clicked=self.addPlayer)
        self.layout.addWidget(buttonAddPlayer)

        self.videoGrid = QGridLayout()
        self.layout.addLayout(self.videoGrid)

        self.player = YouTubePlayer("", parent=self)
        self.videoGrid.addWidget(self.player, 0, 0)
        

        self.layout.addWidget(QLabel(__version__ + " by " + __author__), alignment=Qt.AlignBottom | Qt.AlignRight)
        self.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                height: 40px;
                width: 40px;
                background-color: #E41937;
                color: white;
            }

            * {
                background-color: white;
                font-size: 30px;
            }

            QLineEdir {
                background-color: white;
            }
        
        """)

    def addPlayer(self):
        playerCount = self.videoGrid.count()
        row = playerCount % 3
        col = playerCount // 3

        self.player = YouTubePlayer("", parent=self)
        self.videoGrid.addWidget(self.player, row, col)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Youtubewindow()
    window.show()
    

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Player Window Closed")
