import numpy as np
import matplotlib
import matplotlib.dates as mdates

class GraphManager:
    def __init__(self, ax):
        self.ax = ax

    def set_date_format(self, days_visible):
        """Ajusta o formato da data no eixo x com base no número de dias visíveis."""
        if days_visible <= 7:  # Menos de 1 semana visível
            self.ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%a %d'))
        elif days_visible <= 30:  # Menos de 1 mês visível
            self.ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=3))
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        elif days_visible <= 365:  # Menos de 1 ano visível
            self.ax.xaxis.set_major_locator(mdates.MonthLocator())
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        else:  # Mais de um ano visível
            self.ax.xaxis.set_major_locator(mdates.YearLocator())
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    def update_axis_format(self, event):
        if event is None:
            ax = self.ax
        else:
            ax = event.canvas.figure.axes[0]

        x_min, x_max = ax.get_xlim()
        
        # Usando datetime para calcular a diferença em dias
        date_min = matplotlib.dates.num2date(x_min)
        date_max = matplotlib.dates.num2date(x_max)
        days_visible = (date_max - date_min).days
        
        # Ajusta o formato com base no nível de zoom
        self.set_date_format(days_visible)
        
        self.ax.figure.canvas.draw_idle()