import pandas as pd


class DataScrubber:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def remove_duplicate_records(self) -> pd.DataFrame:
        return self.df.drop_duplicates()
