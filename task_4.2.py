import svgwrite
import cairosvg
import numpy as np
import cv2

def polylines2svg(paths_XYs, svg_path):
    try:
        W, H = 0, 0
        for path_XYs in paths_XYs:
            W, H = max(W, np.max(path_XYs[:, 0])), max(H, np.max(path_XYs[:, 1]))
        
        padding = 0.1
        W, H = int(W + padding * W), int(H + padding * H)
        
        dwg = svgwrite.Drawing(svg_path, profile='tiny', shape_rendering='crispEdges')
        group = dwg.g()
        
        colours = ['red', 'green', 'blue', 'orange', 'purple']
        
        for i, path in enumerate(paths_XYs):
            path_data = []
            c = colours[i % len(colours)]
            path_data.append(f"M {path[0, 0]},{path[0, 1]}")
            for j in range(1, len(path)):
                path_data.append(f"L {path[j, 0]},{path[j, 1]}")
            if not np.allclose(path[0], path[-1]):
                path_data.append("Z")
            group.add(dwg.path(d=' '.join(path_data), fill=c, stroke='none', stroke_width=2))
        
        dwg.add(group)
        dwg.save()
        
        png_path = svg_path.replace('.svg', '.png')
        fact = max(1, 1024 // min(H, W))
        cairosvg.svg2png(url=svg_path, write_to=png_path,
                         parent_width=W, parent_height=H,
                         output_width=fact*W, output_height=fact*H,
                         background_color='white')
        
        print(f"SVG saved to {svg_path}")
        print(f"PNG saved to {png_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "_main_":
    path1 = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    path2 = np.array([[2, 2], [2.5, 2.5], [3, 2], [2.5, 1.5]])

    paths_XYs = [path1, path2]
    svg_path = 'output.svg'


    polylines2svg(paths_XYs, svg_path)