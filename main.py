import sys
import numpy as np
import quandl
from PyQt5.QtCore import QEvent, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QProgressBar, QSizePolicy
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from config import ultima_chamada, contagem_chamadas
from utils.error_handler import show_error_message
from utils.gestures_handler import gestureEvent, pinchTriggered
from data.data_fetcher import DataFetcher
from styles import dark_stylesheet
from utils.plot_helpers import on_zoom
from utils.date_formatting import GraphManager

quandl.ApiConfig.api_key="BQz4-swxyCfNwjrCVsBa"

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_fetcher = DataFetcher(self.plot_data)
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        graph_manager = GraphManager(self.ax)
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas.mpl_connect('draw_event', graph_manager.update_axis_format)
        self.canvas.grabGesture(Qt.PinchGesture)
        self.initUI()
      
    def initUI(self):
        self.setupWindowProperties()
        mainLayout = self.createMainLayout()
        self.setupLoaderWidget()
        self.setupTimerToFetchPrice()
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)
        self.show()

    def setupWindowProperties(self):
        self.setWindowTitle('Preço do Ouro')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet(dark_stylesheet)

    def createMainLayout(self):
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.setContentsMargins(0, 0, 0, 12)
        buttonsLayout.setSpacing(12)

        self.addButtonsToLayout(buttonsLayout)

        mainLayout.addWidget(self.toolbar)
        mainLayout.addWidget(self.canvas)
        mainLayout.addLayout(buttonsLayout)

        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        return mainLayout
    
    def addButtonsToLayout(self, buttonsLayout):
        buttons = [
            ("1W", lambda: self.data_fetcher.fetch_price("7d")),
            ("1M", lambda: self.data_fetcher.fetch_price("30d")),
            ("1Y", lambda: self.data_fetcher.fetch_price("365d")),
            ("ALL", lambda: self.data_fetcher.fetch_price("all"))
        ]

        buttonsLayout.addStretch()

        for text, func in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("margin: 0; padding: 0px; border: 2px solid #fcfcff; border-radius: 8px; color: #fcfcff")
            btn.setFixedSize(48, 48)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(func)
            buttonsLayout.addWidget(btn)

        buttonsLayout.addStretch()

    def setupLoaderWidget(self):
        self.loader = QProgressBar(self)
        self.loader.setFixedSize(200, 24)
        self.loader.setTextVisible(False)
        self.loader.setRange(0, 0)
        self.loader.hide()

        loader_x = (self.width() - self.loader.width()) / 2
        loader_y = (self.height() - self.loader.height()) / 2
        self.loader.move(int(loader_x), int(loader_y))

    def setupTimerToFetchPrice(self):
        QTimer.singleShot(100, lambda: self.data_fetcher.fetch_price("7d"))

    def event(self, event):
        if event.type() == QEvent.Gesture:
            return self.gestureEvent(event)
        return super(App, self).event(event)
    
    def gestureEvent(self, event):
        pinch = event.gesture(Qt.PinchGesture)
        if pinch:
            self.pinchTriggered(pinch)
        return True
    
    def pinchTriggered(self, gesture):
        if gesture.state() == Qt.GestureFinished:
            scaleFactor = gesture.scaleFactor()

            # Recupera os limites atuais dos eixos x e y
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()

            # Calcula os centros dos eixos x e y
            xcenter = (xlim[1] + xlim[0]) / 2
            ycenter = (ylim[1] + ylim[0]) / 2

            # Calcula os novos limites ajustando com base no fator de escala
            xdelta = (xlim[1] - xlim[0]) / 2 / scaleFactor
            ydelta = (ylim[1] - ylim[0]) / 2 / scaleFactor

            # Define os novos limites dos eixos
            self.ax.set_xlim([xcenter - xdelta, xcenter + xdelta])
            self.ax.set_ylim([ycenter - ydelta, ycenter + ydelta])

            self.canvas.draw_idle()
        return True
    
    def plot_data(self, date, price):
        self.ax.clear()
        self.ax.plot(date, price)
        graph_manager = GraphManager(self.ax)
        graph_manager.update_axis_format(None)
        self.canvas.draw()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())