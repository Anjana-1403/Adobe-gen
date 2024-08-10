import numpy as np
import matplotlib.pyplot as plt

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

def normalize_shape(paths_XYs, bounding_size=100):
    normalized_paths = []
    
    for XYs in paths_XYs:
        normalized_XYs = []
        
        all_points = np.vstack(XYs)
        min_x, min_y = np.min(all_points, axis=0)
        max_x, max_y = np.max(all_points, axis=0)
        
        center_x = (max_x + min_x) / 2
        center_y = (max_y + min_y) / 2
        XY_centered = [XY - [center_x, center_y] for XY in XYs]
        
        width = max_x - min_x
        height = max_y - min_y
        
        if width > height:
            scale_factor = bounding_size / width
        else:
            scale_factor = bounding_size / height
        
        XY_normalized = [XY * scale_factor for XY in XY_centered]
        normalized_paths.append(XY_normalized)
    
    return normalized_paths


def write_csv(paths_XYs, output_path):
    with open(output_path, 'w') as f:
        for i, XYs in enumerate(paths_XYs):
            for j, XY in enumerate(XYs):
                for point in XY:
                    f.write(f"{i},{j},{point[0]},{point[1]}\n")

def plot(paths_XYs, title="Data", ax=None):
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))
    colours = ['r', 'g', 'b', 'y', 'm', 'c', 'purple']
    for i, XYs in enumerate(paths_XYs):
        c = colours[i % len(colours)]
        for XY in XYs:
            ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    ax.set_aspect('equal')
    ax.set_title(title)

def main():

    csv_path = r"problems\problems\occlusion1.csv"
    
    original_paths_XYs = read_csv(csv_path)

    processed_paths_XYs = normalize_shape(original_paths_XYs, bounding_size=100)

    output_csv_path = "processed_data.csv"
    write_csv(processed_paths_XYs, output_csv_path)
    
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    plot(original_paths_XYs, title="Original Data", ax=axs[0])
    plot(processed_paths_XYs, title="Processed Data", ax=axs[1])
    plt.show()
    
    print(f"Processed data has been saved to {output_csv_path}")

main()