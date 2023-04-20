"""
Plot the results of the sound correrspondence file evaluation.
"""

import json
import matplotlib.pyplot as plt
import math

def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def find_optimum(points):
    upper_left_corner = (0, 1)
    min_distance = float('inf')
    optimal_point = None

    for point in points:
        distance = euclidean_distance(upper_left_corner, point)
        if distance < min_distance:
            min_distance = distance
            optimal_point = point

    return tuple(optimal_point)

def plot_curve(points, maxfp, maxtp, file_name):
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]

    plt.plot(x_values, y_values, label='ROC Curve')
    plt.xlabel(f'Relative number of guesses per word (100%={maxfp})')
    plt.ylabel(f'Relative number of true positives in data (100%={maxtp})')

    area = auc(points)
    plt.title(f'ROC curve (AUC: {area:.4f})')

    # Find and plot the optimum point
    optimum = find_optimum(points)
    plt.plot(optimum[0], optimum[1], marker='x', color='C1', label='Optimum',
             markersize=10, mew=1)

    plt.legend()
    plt.savefig(file_name, format='jpeg')
    plt.close()

def auc(points):
    points = sorted(points)  # Ensure the points are sorted by x-axis values
    area = 0.0

    for i in range(1, len(points)):
        x1, y1 = points[i - 1]
        x2, y2 = points[i]
        area += (x2 - x1) * (y1 + y2) / 2

    return area

def register(parser):
    """
    """
    parser.add_argument("tpfpjson")
    parser.add_argument("outputjpg")

def run(args):
    with open(args.tpfpjson, "r") as f:
        data = json.load(f)
    plot_curve(data["tp_fp"], data["fp"], data["tp"], args.outputjpg)
