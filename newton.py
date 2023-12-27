
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout,QHBoxLayout, QSlider, QLabel,QSplitter
from PyQt5.QtCore import Qt
from matplotlib import colors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

def getRGB(wavelength,intensity):
        wavelength*=1e9
        waveArea = [400,440,490,510,580,645,780]
        minusWave = [0,440,440,510,510,645,780]
        deltWave = [1,60,50,20,70,65,35]
        for p in range(len(waveArea)):
            if wavelength<waveArea[p]:
                break

        pVar = abs(minusWave[p]-wavelength)/deltWave[p]
        rgbs = [[0,0,0],[pVar,0,1],[0,pVar,1],[0,1,pVar],
                [pVar,1,0],[1,pVar,0],[1,0,0],[0,0,0]]
        
        #在光谱边缘处颜色变暗
        if (wavelength>=380) & (wavelength<420):
            alpha = 0.3+0.7*(wavelength-380)/(420-380)
        elif (wavelength>=420) & (wavelength<701):
            alpha = 1.0
        elif (wavelength>=701) & (wavelength<780):
            alpha = 0.3+0.7*(780-wavelength)/(780-700)
        else:
            alpha = 0       #非可见区

        return colors.rgb2hex([intensity*(c*alpha) for c in rgbs[p]])

class AppDemo(QWidget):    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('牛顿环干涉图样可视化交互系统')
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()

        #入射光波长的滑动条
        self.lambda_slider = QSlider(Qt.Horizontal)
        self.lambda_slider.setMinimum(400)
        self.lambda_slider.setMaximum(760)
        self.lambda_slider.setValue(589)
        self.lambda_slider.setTickInterval(10)
        self.lambda_slider.valueChanged.connect(self.updateGraph)
        layout.addWidget(QLabel(u'入射光波长lambda'))

        lambda_slider_layout = QHBoxLayout()
        lambda_slider_layout.addWidget(QLabel('400nm'))
        lambda_slider_layout.addWidget(self.lambda_slider)
        lambda_slider_layout.addWidget(QLabel('760nm'))
        layout.addLayout(lambda_slider_layout)

        # Add more sliders for other parameters here...
        #透镜曲率半径的滑动条
        self.R_slider=QSlider(Qt.Horizontal)
        self.R_slider.setMinimum(1000)
        self.R_slider.setMaximum(2000)
        self.R_slider.setValue(1500)
        self.R_slider.setTickInterval(1)
        self.R_slider.valueChanged.connect(self.updateGraph)
        layout.addWidget(QLabel(u'透镜曲率半径R'))

        R_slider_layout = QHBoxLayout()
        R_slider_layout.addWidget(QLabel('1.000m'))
        R_slider_layout.addWidget(self.R_slider)
        R_slider_layout.addWidget(QLabel('2.000m'))
        layout.addLayout(R_slider_layout)

        #透镜折射率n1
        self.n1_slider=QSlider(Qt.Horizontal)
        self.n1_slider.setMinimum(140)
        self.n1_slider.setMaximum(180)
        self.n1_slider.setValue(150)
        self.n1_slider.setTickInterval(1)
        self.n1_slider.valueChanged.connect(self.updateGraph)
        layout.addWidget(QLabel(u'透镜折射率n1'))

        n1_slider_layout = QHBoxLayout()
        n1_slider_layout.addWidget(QLabel('1.40'))
        n1_slider_layout.addWidget(self.n1_slider)
        n1_slider_layout.addWidget(QLabel('1.90'))
        layout.addLayout(n1_slider_layout)
        

        #薄膜介质折射率n2
        self.n2_slider=QSlider(Qt.Horizontal)
        self.n2_slider.setMinimum(100)
        self.n2_slider.setMaximum(150)
        self.n2_slider.setValue(100)
        self.n2_slider.setTickInterval(1)
        self.n2_slider.valueChanged.connect(self.updateGraph)
        layout.addWidget(QLabel(u'薄膜介质折射率n2'))

        n1_slider_layout = QHBoxLayout()
        n1_slider_layout.addWidget(QLabel('1.00'))
        n1_slider_layout.addWidget(self.n2_slider)
        n1_slider_layout.addWidget(QLabel('1.50'))
        layout.addLayout(n1_slider_layout)
        

        #透镜与玻璃板最小距离d0
        self.d0_slider=QSlider(Qt.Horizontal)
        self.d0_slider.setMinimum(0)
        self.d0_slider.setMaximum(1000)
        self.d0_slider.setValue(0)
        self.d0_slider.setTickInterval(1)
        self.d0_slider.valueChanged.connect(self.updateGraph)
        layout.addWidget(QLabel(u'透镜与玻璃板最小距离h'))

        n1_slider_layout = QHBoxLayout()
        n1_slider_layout.addWidget(QLabel('0mm'))
        n1_slider_layout.addWidget(self.d0_slider)
        n1_slider_layout.addWidget(QLabel('10mm'))
        layout.addLayout(n1_slider_layout)
        

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        #layout.addWidget(self.canvas)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.lambda_slider)
        splitter.addWidget(self.R_slider)
        splitter.addWidget(self.n1_slider)
        splitter.addWidget(self.n2_slider)
        splitter.addWidget(self.d0_slider)
        splitter.addWidget(self.canvas)
        layout.addWidget(splitter)

        self.setLayout(layout)
        self.ax = self.canvas.figure.subplots()
        self.updateGraph()

        self.setLayout(layout)
    
    

    
   

    def updateGraph(self):
        lambda_val = self.lambda_slider.value() * 1e-9
        R_val=self.R_slider.value()*1e-3

        n1_val=self.n1_slider.value()*1e-2
        n2_val=self.n2_slider.value()*1e-2

        d0_val=self.d0_slider.value()*1e-5
        # Get values from other sliders here...
        x_min = -10e-3 # 观察的最小 x 坐标，单位为 m
        x_max = 10e-3 # 观察的最大 x 坐标，单位为 m
        y_min = -10e-3 # 观察的最小 y 坐标，单位为 m
        y_max = 10e-3 # 观察的最大 y 坐标，单位为 m
        N = 2000 # 观察的点的数量

        # 生成 x 和 y 的坐标数组
        x = np.linspace(x_min, x_max, N)
        y = np.linspace(y_min, y_max, N)
        X, Y = np.meshgrid(x, y)

        # 计算空气层的厚度
        d = R_val / 2 * (1 - np.sqrt(1 - (X**2 + Y**2) / R_val**2)) + d0_val

        # 计算反射光的相位差
        phi = 2 * np.pi * (2 * d / lambda_val+ (n1_val - n2_val) / 2)

        # 计算反射光的强度
        I = np.cos(phi / 2)**2
        # Calculate d, phi, I as before...
        # 创建一个线性分段的颜色映射，传入颜色列表和分段数
        custom_map=colors.LinearSegmentedColormap.from_list('custom_map',[getRGB(lambda_val,i/4) for i in range(0,4)],N=256)
        self.ax.clear()
        self.ax.imshow(I, cmap=custom_map, extent=[x_min, x_max, y_min, y_max])
        self.ax.set_xlabel('x (m)')
        self.ax.set_ylabel('y (m)')
        self.ax.set_title('Newton ring')
        self.canvas.draw()

app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())


