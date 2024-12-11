import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from .downloader import download_youtube_video, reset_download_ui
import pygame  # Para som de clique

def on_enter(event, path):
    event.widget.config(font=('Helvetica', 10, 'underline'))
    play_click_sound()

def on_leave(event):
    event.widget.config(font=('Helvetica', 10))

def play_click_sound():
    pygame.mixer.Sound('assets/click.wav').play()

def create_menu(root, open_download_directory):
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Abrir diretório de downloads", command=open_download_directory)
    file_menu.add_command(label="Sair", command=root.quit)
    menu_bar.add_cascade(label="Arquivo", menu=file_menu)
    root.config(menu=menu_bar)

def open_file(path):
    os.startfile(path)

def update_downloaded_files_list(save_path, downloaded_files_frame):
    for widget in downloaded_files_frame.winfo_children():
        widget.destroy()
    files = os.listdir(save_path)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(save_path, x)), reverse=True)
    for file in files:
        file_path = os.path.join(save_path, file)
        label = tk.Label(downloaded_files_frame, text=file, anchor='w', fg="red", cursor="hand2")
        label.bind("<Enter>", lambda e: on_enter(e, file_path))
        label.bind("<Leave>", lambda e: on_leave(e))
        label.bind("<Button-1>", lambda e, path=file_path: open_file(path))
        label.pack(fill='x')

def start_download(url_entry, quality_var, format_var, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list):
    url = url_entry.get()
    quality = quality_var.get()
    output_format = format_var.get()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira a URL do vídeo.")
        return
    download_youtube_video(url, quality, output_format, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list)
    url_entry.delete(0, tk.END)

def create_gui():
    root = tk.Tk()
    root.title("BaixaTube By Vic")
    root.iconbitmap('assets/icone.ico')

    pygame.mixer.init()

    create_menu(root, lambda: open_download_directory())

    tk.Label(root, text="URL do vídeo do YouTube:").grid(row=0, column=0, padx=10, pady=5)
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=0, column=1, padx=10, pady=5)
    download_button = tk.Button(root, text="Baixar", bg="blue", fg="white", width=10, command=lambda: start_download(
        url_entry, quality_var, format_var, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list))
    download_button.grid(row=0, column=2, padx=10, pady=5)

    open_directory_button = tk.Button(root, text="Abrir diretório de downloads", bg="orange", fg="white", command=lambda: open_download_directory())
    open_directory_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(root, text="Qualidade:").grid(row=2, column=0, padx=10, pady=5)
    quality_var = tk.StringVar(value="best")
    tk.Radiobutton(root, text="Alta qualidade (best)", variable=quality_var, value="best").grid(row=2, column=1, sticky='w')
    tk.Radiobutton(root, text="Média qualidade (worst)", variable=quality_var, value="worst").grid(row=3, column=1, sticky='w')
    tk.Radiobutton(root, text="Somente áudio (bestaudio)", variable=quality_var, value="bestaudio").grid(row=4, column=1, sticky='w')

    tk.Label(root, text="Formato:").grid(row=5, column=0, padx=10, pady=5)
    format_var = tk.StringVar(value="mp4")
    tk.Radiobutton(root, text="MP4", variable=format_var, value="mp4").grid(row=5, column=1, sticky='w')
    tk.Radiobutton(root, text="MP3", variable=format_var, value="mp3").grid(row=6, column=1, sticky='w')

    status_label = tk.Label(root, text="", fg="blue")
    status_label.grid(row=7, column=0, columnspan=3, padx=10, pady=5)

    progress = tk.StringVar()
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
    progress_bar.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

    downloaded_files_frame = tk.Frame(root)
    downloaded_files_frame.grid(row=9, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')

    downloaded_files_canvas = tk.Canvas(downloaded_files_frame)
    scrollbar = ttk.Scrollbar(downloaded_files_frame, orient="vertical", command=downloaded_files_canvas.yview)
    scrollable_frame = ttk.Frame(downloaded_files_canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: downloaded_files_canvas.configure(
            scrollregion=downloaded_files_canvas.bbox("all")
        )
    )

    downloaded_files_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    downloaded_files_canvas.configure(yscrollcommand=scrollbar.set)

    downloaded_files_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(scrollable_frame, text="Arquivos baixados:").pack()

    update_downloaded_files_list(os.path.join(os.getcwd(), 'downloads'))

    root.mainloop()
