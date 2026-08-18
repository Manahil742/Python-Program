
# Dataset : Students Performance in Exams
# Source  : https://www.kaggle.com/datasets/spscientist/students-performance-in-exams

from data_loader import DataLoader
from gui import StudentGUI


def main():
    print("=" * 55)
    print("  Student Performance Analysis System")
    print("=" * 55)

    loader = DataLoader(file_path="StudentsPerformance.csv")
    df = loader.load_data()

    if df is None:
        print(" Could not load StudentsPerformance.csv")
        print(" Make sure the file is in the same folder as main.py")
        return

    print(f"   Rows: {df.shape[0]}  |  Columns: {df.shape[1]}")
    print("=" * 55)

    gui = StudentGUI(df=df)
    gui.launch()


if __name__ == "__main__":
    main()
