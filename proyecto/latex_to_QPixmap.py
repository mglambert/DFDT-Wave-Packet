from PyQt4 import QtGui
import sys
import matplotlib as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg


def latex_to_QPixmap(mathTex, fs):
    # ---- set up a mpl figure instance ----

    fig = mpl.figure.Figure()
    fig.patch.set_facecolor('none')
    fig.set_canvas(FigureCanvasAgg(fig))
    renderer = fig.canvas.get_renderer()

    # ---- plot the mathTex expression ----

    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.patch.set_facecolor('none')
    t = ax.text(0, 0, mathTex, ha='left', va='bottom', fontsize=fs)

    # ---- fit figure size to text artist ----

    fwidth, fheight = fig.get_size_inches()
    fig_bbox = fig.get_window_extent(renderer)

    text_bbox = t.get_window_extent(renderer)

    tight_fwidth = text_bbox.width * fwidth / fig_bbox.width
    tight_fheight = text_bbox.height * fheight / fig_bbox.height

    fig.set_size_inches(tight_fwidth, tight_fheight)

    # ---- convert mpl figure to QPixmap ----

    buf, size = fig.canvas.print_to_buffer()
    qimage = QtGui.QImage.rgbSwapped(QtGui.QImage(buf, size[0], size[1],
                                                  QtGui.QImage.Format_ARGB32))
    qpixmap = QtGui.QPixmap(qimage)

    return qpixmap


if __name__ == '__main__':
    class A(QtGui.QWidget):
        def __init__(self):
            super(A, self).__init__()
            b = "$\epsilon_{r}$"
            self.label = QtGui.QLabel()
            self.label.setParent(self)
            self.label.setPixmap(latex_to_QPixmap(b, 20))


    app = QtGui.QApplication(sys.argv)

    w = A()

    w.show()
    w.resize(700, 200)

    sys.exit(app.exec_())
