import pandas as pd

from config import input_directory
from helper_scripts.smell_helper import get_project_class_smells_in_range, get_project_package_smells_in_range


def count_smells_present_from_start():
    class_smells = get_project_class_smells_in_range()
    package_smells = get_project_package_smells_in_range()
    min_date = min([class_smells.parsedVersionDate.min, class_smells.parsedVersionDate.min])

    class_smells_from_start = class_smells[class_smells.parsedVersionDate == min_date]
    package_smells_from_start = package_smells[package_smells.parsedVersionDate == min_date]
