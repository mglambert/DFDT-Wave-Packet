from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Figura
from PyQt4 import QtGui, QtCore
import matplotlib.gridspec as gridspec
from latex_to_QPixmap import latex_to_QPixmap
from dfdt import dfdt

__author__ = 'Mathias Lambert'


class Simulacion(QtGui.QWidget):
    def __init__(self, celdas_z, celdas_t, parent=None):
        super(Simulacion, self).__init__(parent)

        self.celdas_z = celdas_z
        self.celdas_t = celdas_t
        self.dielectrico = False

        self.label_titulo = QtGui.QLabel("Simulación Wave Packet", self)
        self.label_titulo.setFont(QtGui.QFont("Helvetica", 37, QtGui.QFont.Bold))
        self.label_titulo.move(180, 30)

        self.er1 = QtGui.QDoubleSpinBox(self)
        self.er1.setMinimum(1)
        self.er1.setGeometry(400, 520, 62, 24)
        self.label_er1 = QtGui.QLabel()
        self.label_er1.setParent(self)
        self.label_er1.setPixmap(latex_to_QPixmap("$\epsilon_{r}:$", 20))
        self.label_er1.move(365, 523)

        self.sigma1 = QtGui.QDoubleSpinBox(self)
        self.sigma1.setGeometry(400, 550, 62, 24)
        self.sigma1.setSingleStep(0.01)
        self.label_sigma = QtGui.QLabel()
        self.label_sigma.setParent(self)
        self.label_sigma.setPixmap(latex_to_QPixmap("$\sigma:$", 20))
        self.label_sigma.move(370, 553)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.slider.setParent(self)
        self.slider.setGeometry(110, 490, 631, 22)
        self.slider.setMinimum(0)
        self.slider.setMaximum(celdas_t - 1)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.cambio_slider)

        self.centrar = QtGui.QPushButton("Reset", self)
        self.centrar.setGeometry(679, 50, 81, 32)
        self.centrar.clicked.connect(self._reset)
        self.setear = QtGui.QPushButton("Set Values", self)
        self.setear.move(470, 530)
        self.setear.clicked.connect(self.cambiar_valores)
        self.animacion = QtGui.QPushButton("Animacion", self)
        self.animacion.clicked.connect(self._animacion)

        self.figura = plt.figure()
        self.grafica = Figura(self.figura)
        self.grafica.show()
        self.grafica.setParent(self)
        self.grafica.setGeometry(100, 80, 650, 400)

        self.ex, self.hy = dfdt(celdas_z, celdas_t)
        grid = gridspec.GridSpec(20, 1)
        self.ax = self.figura.add_subplot(grid[:8, :])
        self.ax.hold(False)
        self.ax.plot(self.ex[0], color="red")
        self.ax.set_ylim([-1.5, 1.5])
        self.ax.set_title("Campo Electrico")

        self.ax2 = self.figura.add_subplot(grid[12:, :])
        self.ax2.hold(False)
        self.ax2.plot(self.hy[0], color="blue")
        self.ax2.set_ylim([-1.5, 1.5])
        self.ax2.set_title("Campo Magnetico")

        self.grafica.draw()

        self.setFixedSize(838, 597)

        self.timer = QtCore.QTimer(self)

    def cambio_slider(self):
        d = self.slider.value()
        self.ax.plot(self.ex[d], color="red")
        self.ax.set_ylim([-1.5, 1.5])
        self.ax.set_title("Campo Electrico")

        self.ax2.plot(self.hy[d], color="blue")
        self.ax2.set_ylim([-1.5, 1.5])
        self.ax2.set_title("Campo Magnetico")

        if self.dielectrico:
            self.pintar_area_central()

        self.grafica.draw()

    def _reset(self):
        self.timer.stop()
        self.slider.setValue(0)
        self.ex, self.hy = dfdt(self.celdas_z, self.celdas_t)
        self.er1.setValue(1.)
        self.sigma1.setValue(0.)
        self.dielectrico = False
        self.cambio_slider()

    def pintar_area_central(self):
        self.ax.axvspan(100, 200, alpha=0.25, color="red")
        self.ax2.axvspan(100, 200, alpha=0.25)

    def cambiar_valores(self):
        self.timer.stop()
        epr = self.er1.value()
        sgma = self.sigma1.value()

        if epr != 1. or sgma > 0:
            self.dielectrico = True
        else:
            self.dielectrico = False

        self.ex, self.hy = dfdt(self.celdas_z, self.celdas_t, epsilon_r=epr, sigma=sgma)
        self.slider.setValue(0)
        self.cambio_slider()

    def __animacion(self):
        t = self.slider.value()
        t += 1
        self.slider.setValue(t)
        if t == self.celdas_t - 1:
            self.timer.stop()

    def _animacion(self):
        self.timer.timeout.connect(self.__animacion)
        self.timer.start(1)


if __name__ == "__main__":
    app = QtGui.QApplication([])
    simu = Simulacion(300, 1200)
    simu.show()
    app.exec_()
