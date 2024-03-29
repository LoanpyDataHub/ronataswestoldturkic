"""
Plot the results of the sound correrspondence file evaluation.
"""

import json
import matplotlib.pyplot as plt
import math
from pathlib import Path
from typing import List, Tuple, Union

def euclidean_distance(point1, point2):
    """
    Calculate the `Euclidean distance
    <https://en.wikipedia.org/wiki/Euclidean_distance>`_ between two points.

    :param point1: The first point
    :type point1: a tuple of two integers or floats

    :param point2: The second point
    :type point2: a tuple of two integers or floats

    :return: The euclidean distance
    :rtype: float
    """
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def find_optimum(
        points: List[Tuple[Union[int, float], Union[int, float]]]
        ) -> Tuple[Union[int, float], Union[int, float]]:
    """
    Calculate the euclidean distance of each point to the upper left hand
    corner and return the point with the lowest distance

    :param points: A list of coordinates representing points in the graph.
    :type points: a list of tuples of floats or integers

    :return: The optimal cut-off point of the ROC curve
    :rtype: a tuple of two floats or integers
    """
    upper_left_corner = (0, 1)
    min_distance = float('inf')
    optimal_point = None

    for point in points:
        distance = euclidean_distance(upper_left_corner, point)
        if distance < min_distance:
            min_distance = distance
            optimal_point = point

    return tuple(optimal_point)

def plot_curve(
        points: List[Tuple[Union[int, float], Union[int, float]]],
        absfp: List[int],
        maxtp: int,
        file_name: Union[str, Path]
        ) -> None:
    """

    #. Get a list of x- and y-axis values out of the points argument
    #. Plot them to a graph with matplotlib, add lables to axes.
    #. Calculate the area under the curve and add it to the plot title
    #. Calculate the optimal cut-off point and mark it with an "x" on the
       graph.
    #. Add a legend to the plot and write the image as a jpeg to the specified
       path

    :param points: List of coordinate points as tuples
    :type points: list of tuples of floats or integers

    :param absfp: The absolute numbers of guesses made. Needed to add
                  information to legend on how many guesses are the optimum.
    :type absfp: a list of integers

    :param maxtp: The absolute number of possible true positives. Needed to
                  contextualise the relative information on the plot as a
                  human reader.
    :type maxtp: an integer

    :param file_name: The desired name and location of the output jpeg-file.
    :type file_name: a string or pathlike object

    :return: Writes the images to the specified path, returns None
    :rtype: None

    """
    # get two lists of x-axis and y-axis values
    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]

    # plot graphs and add axis labels
    maxtp = int((maxtp-1) / 2)  # len df - header / nr of cognates per cogset
    plt.plot(x_values, y_values, label='ROC Curve')
    plt.xlabel(f'Relative number of guesses per word (100%={absfp[-1]})')
    plt.ylabel(f'Relative number of true positives in data (100%={maxtp})')

    # get area under the curve and add to plot title
    area = auc(points)
    plt.title(f'Predicting Early Ancient Hungarian forms (AUC: {area:.4f})')

    # Find and plot the optimum point
    optimum = find_optimum(points)
    plt.plot(optimum[0], optimum[1], marker='x', color='C1',
             label=f'Optimum:\nhowmany={absfp[points.index(list(optimum))]}\n(tp: {optimum[1]:.0%})',
             markersize=10, mew=1)

    plt.legend()  # add little info box to bottom right corner
    plt.savefig(file_name, format='jpeg')
    plt.close()

def auc(points: List[Tuple[Union[int, float], Union[int, float]]]) -> float:
    """
    Calculate the area under the curve with the `trapezoidal rule
    <https://en.wikipedia.org/wiki/Trapezoidal_rule>`_

    :param points: A list of x-y-coordinates
    :type points: list of tuples of integers or floats

    :returns: The area under the curve
    :rtype: float

    """
    points = sorted(points)  # Ensure the points are sorted by x-axis values
    area = 0.0

    for i in range(1, len(points)):
        x1, y1 = points[i - 1]
        x2, y2 = points[i]
        area += (x2 - x1) * (y1 + y2) / 2

    return area

def register(parser):
    """
    Register command line arguments and pass them on to the main function.
    Two non-optional arguments will be registered:
    ``srclg`` (source language) and ``tgtlg`` (target langauge).
    Only strings contained in column ``ID`` in ``etc/languages.csv`` are valid
    arguments.
    """
    parser.add_argument("srclg")
    parser.add_argument("tgtlg")

def run(args):
    """

    #. Read file ``loanpy/tpfp{srclg}2{tgtlg}.json`` containing true-positive
       false-positive ratios, the length of the dataframe with header
       ("maxtp") and the guesslist, generated by the ``evalsc`` command.
    #. Plot the data to an ROC-curve, providing the AUC and optimal cut-off.

    """
    with open(f"loanpy/tpfp{args.srclg}2{args.tgtlg}.json", "r") as f:
        data = json.load(f)
    plot_curve(data["tp_fp"], data["fp"], data["tp"],
               f"loanpy/{args.srclg}2{args.tgtlg}.jpeg")
