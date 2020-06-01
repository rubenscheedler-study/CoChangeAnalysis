import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn
import matplotlib.pyplot as plt

from config import input_directory


def threshold_distribution():
    thresholdData = pd.read_csv(input_directory + "/cochanges.csv")
    # get highest threshold
    max_threshold = max(thresholdData['threshold'])
    thresholds = sorted(thresholdData['threshold'])
    print("----threshold results----")
    print("quartile values:")
    firstquartile = np.percentile(thresholds, 25)
    median = np.percentile(thresholds, 50)
    thirdquartile = np.percentile(thresholds, 75)
    print("90% at threshold: ", np.percentile(thresholds, 90))
    print("95% at threshold: ", np.percentile(thresholds, 95))
    print(firstquartile, median, thirdquartile)
    seaborn.violinplot(thresholds)
    plt.title("Violin boxplot of thresholds")
    plt.show()


