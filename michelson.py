# Imports - standard modules
from matplotlib.colors import rgb2hex, LinearSegmentedColormap
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

# Import matplotlib and set it to use Qt5Agg for plotting
import matplotlib as mpl
mpl.use("Qt5Agg")

# Import QtCore QtWidgets from PyQt5

# Import functions from scipy library for scientific simulation

# Import matplotlib backends

# Import pyplot from matplotlib for plotting
# Import rgb2hex to convert rgb into color

# Create a class derived from the FigureCanvas class. This is the canvas on which the sinewaves will be plotted


class MplCanvas(FC):
    def __init__(self, parent=None, width=8, height=6.5, lamda=632, focal=0.2, dist=0.4e-3):
        fig = Figure(figsize=(width, height))

        # Set the figure to the canvas
        FC.__init__(self, fig)
        self.ax = fig.add_subplot()

        # Set some standard figure policies
        FC.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FC.updateGeometry(self)

        # Draw the plot
        self.setLamda(lamda, focal, dist)

    def setLamda(self, lamda, f, d):
        # 创建一个线性分段的颜色映射，传入颜色列表和分段数
        self.cmap = LinearSegmentedColormap.from_list(
            'custom_map', [getRGB(lamda, i/4) for i in range(0, 4)], N=256)

        lamda = lamda/1e9
        self.lamda = lamda
        # 根据公式求出光强分布
        # 求出比较合适的x和y的取值范围
        self.x_max = 25000 * lamda
        self.y_max = 25000 * lamda
        step = 100 * lamda
        x, y = np.meshgrid(np.arange(-self.x_max, self.x_max, step),
                           np.arange(-self.y_max, self.y_max, step))  # 建立坐标网格
        self.r = np.sqrt(x**2 + y**2)

        # 初始化plt
        self.ax.set_xlabel('x (m)')
        self.ax.set_ylabel('y (m)')
        self.ax.set_title('迈克尔逊干涉仿真')

        self.drawPlot(f, d)

    def drawPlot(self, f, d):
        Ir = 4 * (np.cos(2 * np.pi * d / self.lamda *
                  np.cos(np.arctan(self.r / f))))**2  # 光强分布
        self.ax.imshow(Ir/4, cmap=self.cmap,
                       extent=[-self.x_max, self.x_max, -self.y_max, self.y_max])
        # self.ax.colorbar()
        self.draw()

# Define the mainwindow class


class MainApp(QMainWindow):
    def __init__(self):
        """ Constructor or the initializer """
        QMainWindow.__init__(self)

        # Set some default attributes of the window
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("迈克尔逊干涉")

        # define the main widget as self
        self.main_widget = QWidget(self)

        # 添加参数设置部分
        # 波长
        self.loLambda = QVBoxLayout()
        self.lblLambda = QLabel("波长 (nm)", self)
        self.sldLambda = QSlider(Qt.Horizontal)
        self.sldLambda.setMinimum(380)
        self.sldLambda.setMaximum(780)
        self.sldLambda.setValue(632)
        self.sldLambda.setTickPosition(QSlider.TicksBelow)
        self.sldLambda.setTickInterval(5)
        self.edtLambda = QLineEdit(self)
        self.edtLambda.setMaxLength(5)
        self.loLambda.addWidget(self.lblLambda)
        self.loLambda.addSpacing(3)
        self.loLambda.addWidget(self.sldLambda)
        self.loLambda.addSpacing(3)
        self.loLambda.addWidget(self.edtLambda)

        # 两镜距离差
        self.loDist = QVBoxLayout()
        self.lblDist = QLabel("两镜距离差 (1e-4 m)", self)
        self.sldDist = QSlider(Qt.Horizontal)
        self.sldDist.setMinimum(0)
        self.sldDist.setMaximum(160000)
        self.sldDist.setValue(120000)
        self.sldDist.setTickPosition(QSlider.TicksBelow)
        self.sldDist.setTickInterval(1)
        self.edtDist = QLineEdit(self)
        self.edtDist.setMaxLength(5)
        self.loDist.addWidget(self.lblDist)
        self.loDist.addSpacing(3)
        self.loDist.addWidget(self.sldDist)
        self.loDist.addSpacing(3)
        self.loDist.addWidget(self.edtDist)

        # 移动步长
        self.loStep = QVBoxLayout()
        self.lblStep = QLabel("移动步长 (1e-8 m/0.1 s)", self)
        self.sldStep = QSlider(Qt.Horizontal)
        self.sldStep.setMinimum(0)
        self.sldStep.setMaximum(40)
        self.sldStep.setValue(25)
        self.sldStep.setTickPosition(QSlider.TicksBelow)
        self.sldStep.setTickInterval(1)
        self.edtStep = QLineEdit(self)
        self.edtStep.setMaxLength(5)
        self.loStep.addWidget(self.lblStep)
        self.loStep.addSpacing(3)
        self.loStep.addWidget(self.sldStep)
        self.loStep.addSpacing(3)
        self.loStep.addWidget(self.edtStep)

        # 透镜焦距
        self.loFocal = QVBoxLayout()
        self.lblFocal = QLabel("透镜焦距 (m)", self)
        self.edtFocal = QLineEdit(self)
        self.edtFocal.setMaxLength(5)
        self.btnStartMove = QPushButton("开始移动", self)
        self.loFocal.addWidget(self.lblFocal)
        self.loFocal.addSpacing(3)
        self.loFocal.addWidget(self.edtFocal)
        self.loFocal.addSpacing(3)
        self.loFocal.addWidget(self.btnStartMove)

        # 创建一个水平布局，用于容纳参数设置部分
        self.loMichaelson = QHBoxLayout()
        self.loMichaelson.addLayout(self.loLambda)
        self.loMichaelson.addStretch()
        self.loMichaelson.addLayout(self.loDist)
        self.loMichaelson.addStretch()
        self.loMichaelson.addLayout(self.loStep)
        self.loMichaelson.addStretch()
        self.loMichaelson.addLayout(self.loFocal)

        # 获取各个滑动条的数值
        lamda = self.sldLambda.value()
        dist = self.sldDist.value() / 10000 - 8
        step = self.sldStep.value() - 20
        self.edtLambda.setText(str(lamda))
        self.edtDist.setText(str(dist))
        self.edtStep.setText(str(step))
        self.edtFocal.setText('0.2')

        # 移动方法
        self.move = False
        self.timer = QTimer(self)

        # Create an instance of the FigureCanvas
        self.loCanvas = MplCanvas(
            self.main_widget, width=5, height=4, lamda=lamda, focal=0.2, dist=dist/1e4)

        # Set the focus to the main_widget and set it to be central widget
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        # Populate the master layout
        self.loMaster = QVBoxLayout(self.main_widget)
        self.loMaster.addLayout(self.loMichaelson)
        self.loMaster.addWidget(self.loCanvas)

        # Connect slots
        self.sldLambda.valueChanged.connect(self.OnLambdaChanged)
        self.sldDist.valueChanged.connect(self.OnDistChanged)
        self.sldStep.valueChanged.connect(self.OnStepChanged)
        self.edtLambda.editingFinished.connect(self.OnEdtLambdaChanged)
        self.edtDist.editingFinished.connect(self.OnEdtDistChanged)
        self.edtStep.editingFinished.connect(self.OnEdtStepChanged)
        self.edtFocal.editingFinished.connect(self.OnSomethingChanged)
        self.btnStartMove.clicked.connect(self.OnStartButtonClicked)
        self.timer.timeout.connect(self.UpdateDist)

    def OnLambdaChanged(self):
        lamda = self.sldLambda.value()
        self.edtLambda.setText(str(lamda))
        dist = self.sldDist.value() / 10000 - 8
        focal = float(self.edtFocal.text())
        self.loCanvas.setLamda(lamda, focal, dist/1e4)

    def OnDistChanged(self):
        dist = self.sldDist.value() / 10000 - 8
        self.edtDist.setText(str(dist))
        self.OnSomethingChanged()

    def OnStepChanged(self):
        step = self.sldStep.value()
        self.edtStep.setText(str(step-20))
        self.OnSomethingChanged()

    def OnEdtLambdaChanged(self):
        lamda = int(self.edtLambda.text())
        self.sldLambda.setValue(lamda)
        dist = self.sldDist.value() / 10000 - 8
        focal = float(self.edtFocal.text())
        self.loCanvas.setLamda(lamda, focal, dist/1e4)

    def OnEdtDistChanged(self):
        self.sldDist.setValue(int(float(self.edtDist.text())*10000+80000))

    def OnEdtStepChanged(self):
        step = self.edtStep.text()
        self.sldStep.setValue(int(step)+20)

    def OnSomethingChanged(self):
        focal = float(self.edtFocal.text())
        dist = self.sldDist.value() / 10000 - 8
        self.loCanvas.drawPlot(focal, dist/1e4)

    def OnStartButtonClicked(self):
        if self.move == False:
            self.move = True
            self.btnStartMove.setText("停止移动")
            self.timer.start(100)
        else:
            self.move = False
            self.btnStartMove.setText("开始移动")

    def UpdateDist(self):
        if (self.move):
            self.sldDist.setValue(self.sldDist.value() -
                                  self.sldStep.value()-20)


# 由光的波长和光强获取对应的 rgb 值的函数


def getRGB(wavelength, intensity):
    waveArea = [380, 440, 490, 510, 580, 645, 780]
    minusWave = [0, 440, 440, 510, 510, 645, 780]
    deltWave = [1, 60, 50, 20, 70, 65, 35]
    for p in range(len(waveArea)):
        if wavelength < waveArea[p]:
            break

    pVar = abs(minusWave[p]-wavelength)/deltWave[p]
    rgbs = [[0, 0, 0], [pVar, 0, 1], [0, pVar, 1], [0, 1, pVar],
            [pVar, 1, 0], [1, pVar, 0], [1, 0, 0], [0, 0, 0]]

    # 在光谱边缘处颜色变暗
    if (wavelength >= 380) & (wavelength < 420):
        alpha = 0.3+0.7*(wavelength-380)/(420-380)
    elif (wavelength >= 420) & (wavelength < 701):
        alpha = 1.0
    elif (wavelength >= 701) & (wavelength < 780):
        alpha = 0.3+0.7*(780-wavelength)/(780-700)
    else:
        alpha = 0  # 非可见区

    return rgb2hex([intensity*(c*alpha) for c in rgbs[p]])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MyApp = MainApp()
    MyApp.show()
    app.exec()
