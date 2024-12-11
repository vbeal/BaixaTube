import os
import tkinter as tk
from datetime import datetime
from .dialogs import open_file

def on_enter(event, path):
    event.widget.config(font=('Helvetica', 10, 'underline'))

def on_leave(event):
    event.widget.config(font=('Helvetica', 10))

def update_downloaded_files_list(save_path, downloaded_files_frame):
    for widget in downloaded_files_frame.winfo_children():
        widget.destroy()
    files = os.listdir(save_path)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(save_path, x)), reverse=True)
    for file in files:
        file_path = os.path.join(save_path, file)
        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        label = tk.Label(downloaded_files_frame, text=f"{file} - {file_mtime}", anchor='w', fg="red", cursor="hand2", font=('Helvetica', 10, 'bold'))
        label.bind("<Enter>", lambda e: on_enter(e, file_path))
        label.bind("<Leave>", lambda e: on_leave(e))
        label.bind("<Button-1>", lambda e, path=file_path: open_file(path))
        label.pack(fill='x')
