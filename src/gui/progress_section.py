import tkinter as tk
from tkinter import ttk

def create_progress_section(root, progress_bar, status_label, progress):
    status_label = tk.Label(root, text="", fg="blue")
    status_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

    progress = tk.StringVar()
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
