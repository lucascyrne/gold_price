from PyQt5.QtCore import Qt

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
