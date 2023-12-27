# 动态模拟迈克尔逊干涉

# 导入库
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# 确定参数及变量的值
# 单位统一为m
f = 0.2  # 透镜的焦距（单位：m）
lambda_ = 632e-9  # 入射光波长（单位：m）
d = 0.4e-3  # 空气薄膜的厚度 (单位：m)


def main():
    global d
    initPlt()
    while True:
        print(d)
        d -= 0.00005e-3
        drawPlt(d)

# 由光的波长和光强获取对应的 rgb 值的函数


def getRGB(wavelength, intensity):
    wavelength *= 1e9
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

    return mcolors.rgb2hex([intensity*(c*alpha) for c in rgbs[p]])

# 初始化plt


def initPlt():
    global x_max, y_max, r, cmap

    # 根据公式求出光强分布
    x_max = 25000 * lambda_  # x取值范围约为[-12.6mm,12.6mm]
    y_max = 25000 * lambda_  # y取值范围约为[-12.6mm,12.6mm]
    step = 100 * lambda_
    x, y = np.meshgrid(np.arange(-x_max, x_max, step),
                       np.arange(-y_max, y_max, step))  # 建立坐标网格
    r = np.sqrt(x**2 + y**2)

    # 创建一个线性分段的颜色映射，传入颜色列表和分段数
    cmap = mcolors.LinearSegmentedColormap.from_list(
        'custom_map', [getRGB(lambda_, i/4) for i in range(0, 4)], N=256)

    # 初始化plt
    plt.figure(figsize=(8, 8))
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title('Michelson interference pattern')
    drawPlt(d)


def drawPlt(d):
    print(d)
    Ir = 4 * (np.cos(2 * np.pi * d / lambda_ *
              np.cos(np.arctan(r / f))))**2  # 光强分布
    plt.imshow(Ir/4, cmap=cmap, extent=[-x_max, x_max, -y_max, y_max])
    plt.colorbar()
    plt.show()


if __name__ == '__main__':
    main()
