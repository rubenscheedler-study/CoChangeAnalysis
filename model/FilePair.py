class FilePair:
    def __init__(self, file1, file2, start_date, end_date):
        self.file1 = file1
        self.file2 = file2
        self.start_date = start_date
        self.end_date = end_date

    def to_tuple(self):
        return self.file1, self.file2

