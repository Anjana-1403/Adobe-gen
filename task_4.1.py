import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs

def plot(path_XYs, simplify=False):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    for i, XYs in enumerate(path_XYs):
        for XY in XYs:
            if simplify:
                hull = ConvexHull(XY)
                simplified_XY = XY[hull.vertices]
                ax.plot(simplified_XY[:, 0], simplified_XY[:, 1], 'y', linewidth=3)
            else:
                ax.plot(XY[:, 0], XY[:, 1], linewidth=2)
    ax.set_aspect('equal')
    plt.show()

csv_path = r'problems\problems\frag0.csv'  
path_XYs = read_csv(csv_path)

plot(path_XYs, simplify=False)

plot(path_XYs, simplify=True)