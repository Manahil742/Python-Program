# visualizer.py

import matplotlib
matplotlib.use("TkAgg")   # TkAgg backend — required for embedding in Tkinter
import matplotlib.pyplot as plt 
import numpy as np


class Visualizer:
    """
    Generates visualizations for the Students Performance dataset.
    All chart methods return a plt.Figure so Gradio can display them.

    Charts included:
      1. Bar Chart    — Average scores by gender
      2. Histogram    — Math score distribution
      3. Pie Chart    — Gender distribution
      4. Scatter Plot — Math vs Reading score
      5. Line Chart   — Average score per subject
      6. Grouped Bar  — Scores by test preparation course  (Bonus)
      7. Bar Chart    — Performance category counts         (Bonus)
    """

    def __init__(self, df):
        self.__df = df   # Encapsulated

    @property
    def df(self):
        return self.__df

    @df.setter
    def df(self, new_df):
        self.__df = new_df

    def _new_fig(self, figsize=(8, 5)):
        fig, ax = plt.subplots(figsize=figsize)
        return fig, ax

    # 1. Bar Chart — Average Scores by Gender

    def gender_average_scores(self):

        avg = self.__df.groupby("gender")[
            ["math score", "reading score", "writing score"]
        ].mean()

        fig, ax = plt.subplots(figsize=(8, 5))
        avg.plot(kind="bar", ax=ax, color=["#4C72B0", "#DD8452", "#55A868"])
        ax.set_title("Average Scores by Gender", fontsize=14, fontweight="bold")
        ax.set_xlabel("Gender")
        ax.set_ylabel("Average Marks")
        ax.set_xticklabels(avg.index, rotation=0)
        ax.legend(title="Subject")
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        return fig

    # 2. Histogram — Math Score Distribution


    def math_score_distribution(self):

        scores = self.__df["math score"].to_numpy()

        fig, ax = self._new_fig()
        ax.hist(scores, bins=15, color="#4C72B0", edgecolor="black", alpha=0.85)
        ax.set_title("Distribution of Math Scores", fontsize=14, fontweight="bold")
        ax.set_xlabel("Math Score")
        ax.set_ylabel("Number of Students")
        ax.axvline(np.mean(scores), color="red", linestyle="--",
                   linewidth=1.5, label=f"Mean: {np.mean(scores):.1f}")
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        return fig

    # 3. Pie Chart — Gender Distribution

    def gender_distribution(self):

        counts = self.__df["gender"].astype(str).value_counts()

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(
            counts,
            labels=counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#4C72B0", "#DD8452"],
            wedgeprops={"edgecolor": "white", "linewidth": 1.5}
        )
        ax.set_title("Gender Distribution", fontsize=14, fontweight="bold")
        plt.tight_layout()
        return fig

    # 4. Scatter Plot — Math vs Reading Score

    def math_vs_reading(self):

        fig, ax = self._new_fig()
        colors = {"female": "#DD8452", "male": "#4C72B0"}

        for gender, group in self.__df.groupby("gender"):
            ax.scatter(
                group["math score"],
                group["reading score"],
                label=str(gender),
                alpha=0.6,
                color=colors.get(str(gender), "gray"),
                edgecolors="white",
                linewidths=0.4,
                s=40
            )

        ax.set_title("Math Score vs Reading Score", fontsize=14, fontweight="bold")
        ax.set_xlabel("Math Score")
        ax.set_ylabel("Reading Score")
        ax.legend(title="Gender")
        ax.grid(linestyle="--", alpha=0.5)
        plt.tight_layout()
        return fig

    # 5. Line Chart — Average Score Per Subject

    def average_subject_scores(self):

        scores_array = self.__df[
            ["math score", "reading score", "writing score"]
        ].to_numpy()

        averages = np.mean(scores_array, axis=0)
        subjects = ["Math", "Reading", "Writing"]

        fig, ax = self._new_fig()
        ax.plot(subjects, averages, marker="o", color="#4C72B0",
                linewidth=2.5, markersize=9, markerfacecolor="white",
                markeredgewidth=2)

        for i, val in enumerate(averages):
            ax.annotate(f"{val:.1f}", (subjects[i], averages[i]),
                        textcoords="offset points", xytext=(0, 10), ha="center")

        ax.set_title("Average Score Per Subject", fontsize=14, fontweight="bold")
        ax.set_xlabel("Subject")
        ax.set_ylabel("Average Marks")
        ax.set_ylim(0, 100)
        ax.grid(linestyle="--", alpha=0.5)
        plt.tight_layout()
        return fig

    # 6. Grouped Bar — Scores by Test Preparation Course

    def test_prep_scores(self):

        avg = self.__df.groupby("test preparation course")[
            ["math score", "reading score", "writing score"]
        ].mean()

        fig, ax = plt.subplots(figsize=(8, 5))
        avg.plot(kind="bar", ax=ax, color=["#4C72B0", "#DD8452", "#55A868"])
        ax.set_title("Scores by Test Preparation Course", fontsize=14, fontweight="bold")
        ax.set_xlabel("Test Preparation")
        ax.set_ylabel("Average Marks")
        ax.set_xticklabels(avg.index, rotation=0)
        ax.legend(title="Subject")
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        return fig

    # 7. Bar Chart — Performance Category Counts (Bonus)

    def performance_count(self):

        if "Performance" not in self.__df.columns:
            return None

        order  = ["Excellent", "Good", "Average", "Poor"]
        colors = ["#2ecc71",   "#3498db", "#f39c12", "#e74c3c"]
        counts = self.__df["Performance"].value_counts().reindex(order).dropna()

        fig, ax = self._new_fig()
        bars = ax.bar(counts.index, counts.values,
                      color=[colors[order.index(c)] for c in counts.index],
                      edgecolor="white", linewidth=1.2)

        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 5,
                    str(int(bar.get_height())),
                    ha="center", fontsize=11, fontweight="bold")

        ax.set_title("Student Performance Categories", fontsize=14, fontweight="bold")
        ax.set_xlabel("Category")
        ax.set_ylabel("Number of Students")
        ax.set_ylim(0, counts.max() + 50)
        ax.grid(axis="y", linestyle="--", alpha=0.5)
        plt.tight_layout()
        return fig
