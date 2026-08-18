# data_preprocessor.py
# Handles all preprocessing and feature engineering steps.

import pandas as pd
import numpy as np


class DataPreprocessor:
    """
    Cleans, transforms, and engineers features from
    the Students Performance dataset.

    Covers all required preprocessing steps:
      - Missing value handling
      - Duplicate removal
      - Data type conversion
      - Filtering and sorting
      - Feature engineering
    """

    def __init__(self, df):
        self.__df = df.copy()   # Encapsulated — original df is never modified

    # Getter

    @property #
    def df(self):
        return self.__df

    # 1. Handle Missing Values


    def handle_missing_values(self):
        
        numeric_cols     = self.__df.select_dtypes(include=["int64", "float64"]).columns
        categorical_cols = self.__df.select_dtypes(include=["object", "category"]).columns

        for col in numeric_cols:
            mean_val = np.mean(self.__df[col].dropna().to_numpy())
            self.__df[col] = self.__df[col].fillna(mean_val)

        for col in categorical_cols:
            mode_val = self.__df[col].mode()[0]
            self.__df[col] = self.__df[col].fillna(mode_val)

        return self.__df

    # 2. Remove Duplicates

    def remove_duplicates(self):
        before = len(self.__df)
        self.__df.drop_duplicates(inplace=True) # Remove duplicate rows
        self.__df.reset_index(drop=True, inplace=True) 
        after = len(self.__df) 
        print(f"[Preprocessor] Removed {before - after} duplicate(s).")
        return self.__df

    # 3. Data Type Conversion


    def convert_data_types(self):
        score_cols = ["math score", "reading score", "writing score"]
        for col in score_cols:
            if col in self.__df.columns:
                self.__df[col] = self.__df[col].astype(int)

        cat_cols = [
            "gender",
            "race/ethnicity",
            "parental level of education",
            "lunch",
            "test preparation course",
        ]
        for col in cat_cols: #
            if col in self.__df.columns: 
                self.__df[col] = self.__df[col].astype("category")

        return self.__df
    
    # 4. Feature Engineering

    def create_average_score(self):
        scores_array = self.__df[
            ["math score", "reading score", "writing score"]
        ].to_numpy()
                                                                    #row wise avg
        self.__df["Average Score"] = np.round(np.mean(scores_array, axis=1), 2)
        return self.__df

    def add_performance_label(self):
        """
        Add 'Performance' label based on Average Score:
          >= 80  → Excellent
          >= 60  → Good
          >= 40  → Average
          < 40   → Poor
        """
        if "Average Score" not in self.__df.columns:
            self.create_average_score()

        conditions = [
            self.__df["Average Score"] >= 80,
            self.__df["Average Score"] >= 60,
            self.__df["Average Score"] >= 40,
        ]
        choices = ["Excellent", "Good", "Average"]
        self.__df["Performance"] = np.select(conditions, choices, default="Poor")
        return self.__df

    def add_pass_fail(self):
        scores = self.__df[["math score", "reading score", "writing score"]].to_numpy()
        self.__df["Pass/Fail"] = np.where(
            np.all(scores >= 40, axis=1), "Pass", "Fail"
        )
        return self.__df


    # 5. Filtering and Sorting
 

    def filter_by_gender(self, gender):
        return self.__df[
            self.__df["gender"].astype(str).str.lower() == gender.lower()
        ]

    def filter_by_performance(self, label):
        if "Performance" not in self.__df.columns:
            self.add_performance_label()
        return self.__df[self.__df["Performance"] == label]

    def sort_by_average(self, ascending=False):
        if "Average Score" not in self.__df.columns:
            self.create_average_score()
        self.__df = self.__df.sort_values(
            by="Average Score", ascending=ascending
        ).reset_index(drop=True)
        return self.__df

    def top_students(self, n=10):
        if "Average Score" not in self.__df.columns:
            self.create_average_score()
        return self.__df.nlargest(n, "Average Score")

    # Run All Preprocessing Steps at Once

    def run_all(self):
        self.handle_missing_values()
        self.remove_duplicates()
        self.convert_data_types()
        self.create_average_score()
        self.add_performance_label()
        self.add_pass_fail()
        return self.__df

    def dataset_summary(self):
        return self.__df.describe(include="all")

    def missing_value_report(self):
        report = self.__df.isnull().sum().to_frame(name="Missing Values")
        report["% Missing"] = (report["Missing Values"] / len(self.__df) * 100).round(2)
        return report.reset_index().rename(columns={"index": "Column"})
