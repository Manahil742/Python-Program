# gui.py
# Tkinter-based GUI for the Student Performance Analysis app.

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore


from data_loader import DataLoader  # type: ignore
from data_preprocessor import DataPreprocessor  # type: ignore
from visualizer import Visualizer  # type: ignore


class StudentGUI:
    """
    Tkinter GUI for the Student Performance Analysis System.
    """

    def __init__(self, df=None):
        self.__loader    = DataLoader() #an object that loads datasets.
        self.__processor = None #will later store the preprocessing object.
        self.__viz       = None
        self.__df        = None

        # Root window
        self.__root = tk.Tk() #creates the main window
        self.__root.title("Student Performance Analysis System")
        self.__root.geometry("1200x700") #width/height
        self.__root.configure(bg="#f0f4f8")

        self.__canvas_widget = None   #Used to store graphs

        self._build_ui() #Creates all buttons, panels, and labels

        if df is not None:
            self._init_components(df) #creates objects after loading data
            self._show_status(f"Dataset loaded — {df.shape[0]} rows x {df.shape[1]} columns")
            self._display_df(df.head(20))


    def _init_components(self, df):
        self.__df        = df #Stores dataset
        self.__processor = DataPreprocessor(df) #creates preprocessing object
        self.__viz       = Visualizer(df) #creates visualization object

    def _sync(self): #when the DataFrame is modified, update the processor and visualizer
        if self.__processor:
            self.__df      = self.__processor.df
            self.__viz.df  = self.__df

    def _ready(self): #check if a dataset is loaded
        return self.__df is not None

    def _show_status(self, msg): #display a message in the status bar
        self.__status_var.set(msg)

    def _require_loaded(self):
        if not self._ready():
            messagebox.showwarning("No Data", "Please load the dataset first.")
            return False
        return True


    def _clear_right(self): #delete all widgets in the right frame (used before displaying new content)
        for widget in self.__right_frame.winfo_children():
            widget.destroy()
        self.__canvas_widget = None

    def _display_df(self, df):
        self._clear_right()

        # Scrollbars
        vsb = ttk.Scrollbar(self.__right_frame, orient="vertical")
        hsb = ttk.Scrollbar(self.__right_frame, orient="horizontal")
        vsb.pack(side="right",  fill="y")
        hsb.pack(side="bottom", fill="x")

        cols = list(df.columns)
        tree = ttk.Treeview( #Treeview is used to display data in rows and columns
            self.__right_frame, #place it inside right frame
            columns=cols,
            show="headings", #display only the headings, no tree structure
            yscrollcommand=vsb.set, #connect vertical scrollbar to treeview
            xscrollcommand=hsb.set
        )
        vsb.config(command=tree.yview) 
        hsb.config(command=tree.xview)

        for col in cols:
            tree.heading(col, text=col) #display column names as headings
            tree.column(col, width=130, anchor="center") #define column width and alignment
            # _ means receiving the index, but I don't need to use it        
                    #loops through each row of the Data
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row)) #displays the row values in the treeview

        tree.pack(fill="both", expand=True) #allow the treeview to expand and fill the right frame

    def _display_chart(self, fig):
        self._clear_right()
        canvas = FigureCanvasTkAgg(fig, master=self.__right_frame) #define a canvas to display the Matplotlib figure inside the right frame
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.__canvas_widget = canvas #store the canvas widget so we can clear it later when displaying new content


    def _build_ui(self):
        title = tk.Label(
            self.__root,
            text="Student Performance Analysis System",
            font=("Helvetica", 16, "bold"),
            bg="#2c3e50", fg="white",
            pady=10
        )
        title.pack(fill="x") #display the title at the top of the window, stretching across the width

        main = tk.Frame(self.__root, bg="#f0f4f8") #main frame that will hold the left and right panels
        main.pack(fill="both", expand=True, padx=10, pady=5)

        # Left panel
        left = tk.Frame(main, bg="#f0f4f8", width=220)
        left.pack(side="left", fill="y", padx=(0, 8))
        left.pack_propagate(False) #prevents the left frame from resizing based on its content, keeping it at a fixed width of 220 pixels.

        # Right panel
        self.__right_frame = tk.Frame(main, bg="white", relief="flat", bd=1)
        self.__right_frame.pack(side="left", fill="both", expand=True)

        #A StringVar stores text that can change automatically
        self.__status_var = tk.StringVar(value="Ready — load the dataset to begin.")
        status_bar = tk.Label(
            self.__root,
            textvariable=self.__status_var, #display the status message,instead of fixed text
            font=("Helvetica", 10),
            bg="#2c3e50", fg="#ecf0f1",
            anchor="w", padx=10, pady=4
        )
        status_bar.pack(fill="x", side="bottom")

        self._build_left_panel(left)

    def _section_label(self, parent, text): #a helper function,Instead of writing the same label code repeatedly, you call
        tk.Label(
            parent, text=text,
            font=("Helvetica", 10, "bold"),
            bg="#2c3e50", fg="white",
            anchor="w", padx=6, pady=3
        ).pack(fill="x", pady=(10, 2))

    def _btn(self, parent, text, command, color="#3498db"):
        tk.Button(
            parent, text=text, command=command,
            font=("Helvetica", 9),
            bg=color, fg="white",
            activebackground="#2980b9", activeforeground="white",#Changes the background color while the button is being clicked
            relief="flat", cursor="hand2", #changes the cursor to a hand when hovering over the button
            padx=6, pady=5
        ).pack(fill="x", pady=2)

    def _build_left_panel(self, parent):

        self._section_label(parent, "LOAD DATASET")
        self._btn(parent, "Load Dataset (CSV)",   self.load_dataset,   "#27ae60") #loads the dataset from a CSV file
        self._btn(parent, "Preview Dataset",       self.show_preview) #Displays the dataset
        self._btn(parent, "Dataset Info",          self.show_info)

        self._section_label(parent, "EXPLORE")
        self._btn(parent, "Statistical Summary",   self.show_summary)
        self._btn(parent, "Missing Values",        self.show_missing)
        self._btn(parent, "Data Types",            self.show_dtypes)

        self._section_label(parent, "PREPROCESS")
        self._btn(parent, "Clean Data",            self.run_clean,          "#e67e22")
        self._btn(parent, "Convert Data Types",    self.run_convert_types,  "#e67e22")
        self._btn(parent, "Create Average Score",  self.run_average,        "#e67e22")
        self._btn(parent, "Add Performance Label", self.run_performance,    "#e67e22")
        self._btn(parent, "Add Pass / Fail",       self.run_pass_fail,      "#e67e22")
        self._btn(parent, "Sort by Average",       self.run_sort,           "#e67e22")
        self._btn(parent, "Top 10 Students",       self.run_top_students,   "#8e44ad")
        self._btn(parent, "Run ALL Steps",      self.run_all,            "#c0392b")

        self._section_label(parent, "VISUALIZATIONS")
        self._btn(parent, "Bar  — Scores by Gender",      self.chart_bar)
        self._btn(parent, "Histogram — Math Scores",      self.chart_histogram)
        self._btn(parent, "Pie  — Gender Split",          self.chart_pie)
        self._btn(parent, "Scatter — Math vs Reading",    self.chart_scatter)
        self._btn(parent, "Line — Subject Averages",      self.chart_line)
        self._btn(parent, "Bar  — Test Prep Impact",      self.chart_test_prep)
        self._btn(parent, " Performance Categories",   self.chart_performance, "#8e44ad")



    def load_dataset(self):
        path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not path:
            return

        df = self.__loader.load_data(file_path=path)
        if df is None:
            messagebox.showerror("Error", "Failed to load the selected file.")
            return

        self._init_components(df) #stores the loaded dataset in the processor and visualizer
        self._show_status(f" Loaded: {path}  |  {df.shape[0]} rows x {df.shape[1]} columns")
        self._display_df(df.head(20))



    def show_preview(self):
        if not self._require_loaded(): return
        self._display_df(self.__df.head(20))
        self._show_status(f"Preview — first 20 of {len(self.__df)} rows.")

    def show_info(self):
        if not self._require_loaded(): return
        info = self.__loader.dataset_info(self.__df) #get dataset info as a dictionary
        import pandas as pd
        rows = [{"Property": k, "Value": str(v)} for k, v in info.items()
                if k not in ("Data Types", "Column Names")]
        for col, dtype in info["Data Types"].items():
            rows.append({"Property": f"dtype: {col}", "Value": dtype})
        self._display_df(pd.DataFrame(rows))
        self._show_status("Dataset info displayed.")

    def show_summary(self):
        if not self._require_loaded(): return
        self._display_df(self.__df.describe(include="all").reset_index())
        self._show_status("Statistical summary.")

    def show_missing(self):
        if not self._require_loaded(): return
        self._display_df(self.__processor.missing_value_report())
        self._show_status("Missing value report.")

    def show_dtypes(self):
        if not self._require_loaded(): return
        import pandas as pd
        dtypes = self.__df.dtypes.reset_index()
        dtypes.columns = ["Column", "Data Type"]
        dtypes["Data Type"] = dtypes["Data Type"].astype(str)
        self._display_df(dtypes)
        self._show_status("Column data types.")



    def run_clean(self):
        if not self._require_loaded(): return
        self.__processor.handle_missing_values()
        self.__processor.remove_duplicates()
        self._sync()
        self._display_df(self.__df.head(20))
        self._show_status(" Missing values filled & duplicates removed.")

    def run_convert_types(self):
        if not self._require_loaded(): return
        self.__processor.convert_data_types()
        self._sync()
        import pandas as pd
        dtypes = self.__df.dtypes.reset_index()
        dtypes.columns = ["Column", "Data Type"]
        dtypes["Data Type"] = dtypes["Data Type"].astype(str)
        self._display_df(dtypes)
        self._show_status(" Data types converted.")

    def run_average(self):
        if not self._require_loaded(): return
        self.__processor.create_average_score()
        self._sync()
        self._display_df(self.__df[["math score", "reading score",
                                    "writing score", "Average Score"]].head(20))
        self._show_status(" 'Average Score' column created.")

    def run_performance(self):
        if not self._require_loaded(): return
        self.__processor.add_performance_label()
        self._sync()
        self._display_df(self.__df[["math score", "reading score",
                                    "writing score", "Average Score",
                                    "Performance"]].head(20))
        self._show_status(" 'Performance' labels added.")

    def run_pass_fail(self):
        if not self._require_loaded(): return
        self.__processor.add_pass_fail()
        self._sync()
        self._display_df(self.__df[["math score", "reading score",
                                    "writing score", "Pass/Fail"]].head(20))
        self._show_status(" 'Pass/Fail' column added.")

    def run_sort(self):
        if not self._require_loaded(): return
        self.__processor.sort_by_average()
        self._sync()
        self._display_df(self.__df.head(20))
        self._show_status(" Sorted by Average Score (descending).")

    def run_top_students(self):
        if not self._require_loaded(): return
        self._display_df(self.__processor.top_students(n=10))
        self._show_status("Top 10 students by Average Score.")

    def run_all(self):
        if not self._require_loaded(): return
        self.__processor.run_all()
        self._sync()
        self._display_df(self.__df.head(20))
        self._show_status(" Full pipeline done — cleaned, typed, scored, labelled.")


    def _ensure_performance(self):
        if "Performance" not in self.__df.columns:
            self.__processor.add_performance_label()
            self._sync()

    def chart_bar(self):
        if not self._require_loaded(): return
        self._sync()
        self._display_chart(self.__viz.gender_average_scores())
        self._show_status("Bar chart — Average scores by gender.")

    def chart_histogram(self):
        if not self._require_loaded(): return
        self._sync()
        self._display_chart(self.__viz.math_score_distribution())
        self._show_status("Histogram — Math score distribution.")

    def chart_pie(self):
        if not self._require_loaded(): return
        self._sync()
        self._display_chart(self.__viz.gender_distribution())
        self._show_status("Pie chart — Gender distribution.")

    def chart_scatter(self):
        if not self._require_loaded(): return
        self._sync()
        self._display_chart(self.__viz.math_vs_reading())
        self._show_status("Scatter plot — Math vs Reading score.")

    def chart_line(self):
        if not self._require_loaded(): return
        self._sync()
        self._display_chart(self.__viz.average_subject_scores())
        self._show_status("Line chart — Average score per subject.")

    def chart_test_prep(self):
        if not self._require_loaded(): return
        self._sync()
        self._display_chart(self.__viz.test_prep_scores())
        self._show_status("Bar chart — Scores by test preparation course.")

    def chart_performance(self):
        if not self._require_loaded(): return
        self._ensure_performance()
        fig = self.__viz.performance_count()
        if fig:
            self._display_chart(fig)
            self._show_status("Performance category counts.")
        else:
            messagebox.showwarning("Warning", "Run preprocessing first to generate Performance labels.")


    def launch(self):
        self.__root.mainloop()
