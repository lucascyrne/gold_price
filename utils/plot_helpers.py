import numpy as np

def on_zoom(self, event):
  x_min, x_max = self.ax.get_xlim()
  delta = x_max - x_min
  days_visible = (np.timedelta64(int(delta), 'ns') / np.timedelta64(1, 'D')).astype(int)
  self.set_date_format(days_visible)
  self.canvas.draw_idle()
