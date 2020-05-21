from ClassFOAnalysis import ClassFOAnalysis
from FOAnalyzer import FOAnalyzer
from PackageFOAnalysis import PackageFOAnalysis


class CombinedFOAnalysis:

    def __init__(self):
        self.analyzer = FOAnalyzer()
        self.classAnalyzer = ClassFOAnalysis()
        self.package_analyzer = PackageFOAnalysis()

    # Executes a range of relevant tests on class-level co-changes and smells.
    def execute(self):
        class_smelling_co_changing_pairs, class_all_smelly_pairs, class_co_changed_pairs, class_all_pairs = self.classAnalyzer.get_pairs()
        package_smelling_co_changing_pairs, package_all_smelly_pairs, package_co_changed_pairs, package_all_pairs = self.classAnalyzer.get_pairs()
        # Sum the two lists for each cont. table value
        smelling_co_changing_pairs = class_smelling_co_changing_pairs + package_smelling_co_changing_pairs
        all_smelly_pairs = class_all_smelly_pairs + package_all_smelly_pairs
        co_changed_pairs = class_co_changed_pairs + package_co_changed_pairs
        all_pairs = class_all_pairs + package_all_pairs

        print("combined analysis results:")
        self.analyzer.analyze_results(smelling_co_changing_pairs, all_smelly_pairs, co_changed_pairs, all_pairs)
