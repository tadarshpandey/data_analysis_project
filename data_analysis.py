import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import seaborn as sns
import numpy as np

class DataAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Analysis Dashboard")
        self.root.geometry("1200x800")
        
        # Initialize data variables
        self.data = None
        self.file_path = None
        
        # Create main container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create navigation bar
        self.create_navbar()
        
        # Create content frame
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Show home screen initially
        self.show_home()
    
    def create_navbar(self):
        """Create the navigation bar"""
        navbar = ttk.Frame(self.main_frame)
        navbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Navigation buttons
        ttk.Button(navbar, text="Home", command=self.show_home).pack(side=tk.LEFT, padx=5)
        ttk.Button(navbar, text="Data Overview", command=self.show_data_overview).pack(side=tk.LEFT, padx=5)
        ttk.Button(navbar, text="Numerical Analysis", command=self.show_numerical_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(navbar, text="Categorical Analysis", command=self.show_categorical_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(navbar, text="Correlation Analysis", command=self.show_correlation_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(navbar, text="Visualizations", command=self.show_visualizations).pack(side=tk.LEFT, padx=5)
        
        # File operations
        ttk.Button(navbar, text="Load CSV", command=self.load_csv).pack(side=tk.RIGHT, padx=5)
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home(self):
        """Show home screen"""
        self.clear_content()
        
        ttk.Label(self.content_frame, 
                 text="Data Analysis Dashboard", 
                 font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        ttk.Label(self.content_frame, 
                 text="Load a CSV file to begin analysis", 
                 font=('Helvetica', 12)).pack(pady=10)
        
        ttk.Button(self.content_frame, 
                  text="Browse CSV File", 
                  command=self.load_csv).pack(pady=20)
        
        if self.file_path:
            ttk.Label(self.content_frame, 
                     text=f"Loaded file: {self.file_path}", 
                     font=('Helvetica', 10)).pack(pady=5)
    
    def load_csv(self):
        """Load a CSV file"""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "student_data.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.file_path = file_path
                messagebox.showinfo("Success", "CSV file loaded successfully!")
                self.show_home()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def show_data_overview(self):
        """Show data overview"""
        self.clear_content()
        
        if self.data is None:
            self.show_no_data_message()
            return
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Basic Info
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Basic Info")
        
        # Add content to tab1
        info_text = f"""Number of rows: {len(self.data)}
Number of columns: {len(self.data.columns)}
Columns: {', '.join(self.data.columns)}"""
        
        ttk.Label(tab1, text=info_text, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=10)
        
        # Tab 2: First 5 Rows
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Sample Data")
        
        # Display first 5 rows in a treeview
        columns = list(self.data.columns)
        tree = ttk.Treeview(tab2, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        for i, row in self.data.head().iterrows():
            tree.insert("", tk.END, values=list(row))
        
        scrollbar = ttk.Scrollbar(tab2, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
    
    def show_numerical_analysis(self):
        """Show numerical analysis"""
        self.clear_content()
        
        if self.data is None:
            self.show_no_data_message()
            return
        
        numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        if len(numerical_cols) == 0:
            ttk.Label(self.content_frame, text="No numerical columns found!").pack()
            return
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab for each numerical column
        for col in numerical_cols:
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=col)
            
            # Statistics frame
            stats_frame = ttk.LabelFrame(tab, text="Statistics")
            stats_frame.pack(fill=tk.X, padx=10, pady=5)
            
            stats_text = f"""Mean: {self.data[col].mean():.2f}
Median: {self.data[col].median():.2f}
Std Dev: {self.data[col].std():.2f}
Min: {self.data[col].min():.2f}
Max: {self.data[col].max():.2f}"""
            
            ttk.Label(stats_frame, text=stats_text, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=10)
            
            # Visualization frame
            vis_frame = ttk.LabelFrame(tab, text="Visualizations")
            vis_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            
            # Histogram
            self.data[col].hist(ax=ax1, bins=20)
            ax1.set_title(f'Histogram of {col}')
            
            # Box plot
            self.data.boxplot(column=col, ax=ax2)
            ax2.set_title(f'Box Plot of {col}')
            
            plt.tight_layout()
            
            # Embed plot in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=vis_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_categorical_analysis(self):
        """Show categorical analysis"""
        self.clear_content()
        
        if self.data is None:
            self.show_no_data_message()
            return
        
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) == 0:
            ttk.Label(self.content_frame, text="No categorical columns found!").pack()
            return
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab for each categorical column
        for col in categorical_cols:
            tab = ttk.Frame(notebook)
            notebook.add(tab, text=col)
            
            # Value counts frame
            counts_frame = ttk.LabelFrame(tab, text="Value Counts")
            counts_frame.pack(fill=tk.X, padx=10, pady=5)
            
            counts = self.data[col].value_counts()
            counts_text = "\n".join([f"{val}: {count}" for val, count in counts.items()])
            
            ttk.Label(counts_frame, text=counts_text, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=10)
            
            # Visualization frame
            vis_frame = ttk.LabelFrame(tab, text="Distribution")
            vis_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            
            fig, ax = plt.subplots(figsize=(8, 5))
            counts.plot(kind='bar', ax=ax)
            ax.set_title(f'Distribution of {col}')
            ax.tick_params(axis='x', rotation=45)
            plt.tight_layout()
            
            # Embed plot in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=vis_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_correlation_analysis(self):
        """Show correlation analysis"""
        self.clear_content()
        
        if self.data is None:
            self.show_no_data_message()
            return
        
        numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        if len(numerical_cols) < 2:
            ttk.Label(self.content_frame, text="Need at least 2 numerical columns for correlation analysis!").pack()
            return
        
        # Create frame for correlation analysis
        main_frame = ttk.Frame(self.content_frame)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Correlation heatmap
        fig, ax = plt.subplots(figsize=(8, 6))
        corr = self.data[numerical_cols].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax)
        ax.set_title('Correlation Heatmap')
        
        # Embed plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=main_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Show top correlations
        corr_frame = ttk.LabelFrame(self.content_frame, text="Top Correlations")
        corr_frame.pack(fill=tk.X, padx=10, pady=5)
        
        corr_matrix = self.data[numerical_cols].corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        top_correlations = upper.unstack().sort_values(ascending=False).dropna()
        
        text = "\n".join([f"{pair[0]} & {pair[1]}: {val:.2f}" 
                         for pair, val in top_correlations.head(5).items()])
        
        ttk.Label(corr_frame, text=text, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=10)
    
    def show_visualizations(self):
        """Show all visualizations"""
        self.clear_content()
        
        if self.data is None:
            self.show_no_data_message()
            return
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.content_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Numerical visualizations
        numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        if len(numerical_cols) > 0:
            num_tab = ttk.Frame(notebook)
            notebook.add(num_tab, text="Numerical")
            
            # Create a canvas with scrollbar
            canvas = tk.Canvas(num_tab)
            scrollbar = ttk.Scrollbar(num_tab, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Add visualizations for each numerical column
            for col in numerical_cols:
                frame = ttk.LabelFrame(scrollable_frame, text=col)
                frame.pack(fill=tk.X, padx=10, pady=5)
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
                
                # Histogram
                self.data[col].hist(ax=ax1, bins=20)
                ax1.set_title(f'Histogram of {col}')
                
                # Box plot
                self.data.boxplot(column=col, ax=ax2)
                ax2.set_title(f'Box Plot of {col}')
                
                plt.tight_layout()
                
                # Embed plot in Tkinter
                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Categorical visualizations
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            cat_tab = ttk.Frame(notebook)
            notebook.add(cat_tab, text="Categorical")
            
            # Create a canvas with scrollbar
            canvas = tk.Canvas(cat_tab)
            scrollbar = ttk.Scrollbar(cat_tab, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Add visualizations for each categorical column
            for col in categorical_cols:
                frame = ttk.LabelFrame(scrollable_frame, text=col)
                frame.pack(fill=tk.X, padx=10, pady=5)
                
                fig, ax = plt.subplots(figsize=(8, 5))
                counts = self.data[col].value_counts()
                counts.plot(kind='bar', ax=ax)
                ax.set_title(f'Distribution of {col}')
                ax.tick_params(axis='x', rotation=45)
                plt.tight_layout()
                
                # Embed plot in Tkinter
                canvas = FigureCanvasTkAgg(fig, master=frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_no_data_message(self):
        """Show message when no data is loaded"""
        self.clear_content()
        ttk.Label(self.content_frame, 
                 text="No data loaded! Please load a CSV file first.", 
                 font=('Helvetica', 12)).pack(pady=50)
        ttk.Button(self.content_frame, 
                  text="Load CSV File", 
                  command=self.load_csv).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = DataAnalysisApp(root)
    root.mainloop()