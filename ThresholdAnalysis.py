import csv
import matplotlib.pyplot as plt
import numpy as np

from config import input_directory


def threshold_distribution():
    # read csv
    with open(input_directory + '/cochanges.csv', newline='') as csv_file:
        thresholdData = list(csv.reader(csv_file))[1:]
    thresholds = list(map(lambda x: int(x), list(zip(*thresholdData))[2]))
    # get highest threshold
    max_threshold = max(thresholds)
    thresholds = sorted(thresholds)
    plt.hist(thresholds, bins=range(0, max_threshold + 1))
    plt.title("Cochange match count distribution")
    plt.show()
    print("----threshold results----")
    print("quartile values:")
    firstquartile = np.percentile(thresholds, 25)
    median = np.percentile(thresholds, 50)
    thirdquartile = np.percentile(thresholds, 75)
    print("90% at threshold: ", np.percentile(thresholds, 90))
    print("95% at threshold: ", np.percentile(thresholds, 95))
    print(firstquartile, median, thirdquartile)


