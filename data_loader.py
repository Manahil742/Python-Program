# data_loader.py
# Handles loading and basic inspection of the dataset.

import pandas as pd
import numpy as np
import os #used for file path handling and checking if the file exists


class DataLoader:

    def __init__(self, file_path="StudentsPerformance.csv"):
        self.__file_path = file_path   # Encapsulated attribute
        self.__df = None #private variable for the dataset

    # Load Dataset


    def load_data(self, file_path=None): #Allows loading a different file if a path is provided, otherwise uses the default path set in the constructor
        if file_path:
            self.__file_path = file_path

        try:
            self.__df = pd.read_csv(self.__file_path)
            print(f"[DataLoader] Dataset loaded: {self.__file_path}")
            return self.__df

        except FileNotFoundError:
            print(f"[DataLoader] File not found: {self.__file_path}")
            return None

        except Exception as e: #Catches any other exceptions that may occur during loading and prints the error message
            print(f"[DataLoader] Error loading file: {e}")
            return None

    # Dataset Information
 

    def dataset_info(self, df):
        info = {
            "Rows"        : df.shape[0], #Number of rows in the dataset
            "Columns"     : df.shape[1],
            "Column Names": list(df.columns), #List of column names in the dataset
            "Data Types"  : df.dtypes.astype(str).to_dict(),
        }
        return info

    def preview_data(self, df, rows=5):
        return df.head(rows)

    def get_file_path(self):
        return self.__file_path #returns the current file path being used by the DataLoader
