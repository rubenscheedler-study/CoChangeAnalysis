import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from FOAnalysis import find_smelly_pairs_with_date
from config import analysis_start_date, analysis_end_date


# Plots a histogram of arch. smells over time.
def smells_over_time():
    smell_pairs = find_smelly_pairs_with_date(analysis_start_date, analysis_end_date)
    years_of_smells = smell_pairs.parsedVersionDate.map(lambda d: d.year)
    plt.hist(years_of_smells)
    plt.show()


smells_over_time()
