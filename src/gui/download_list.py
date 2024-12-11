import os
import tkinter as tk
from datetime import datetime
from .dialogs import open_file
from .list_utils import on_enter, on_leave, update_downloaded_files_list


def start_download(url_entry, quality_var, format_var, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list, downloaded_files_frame):
    url = url_entry.get()
    quality = quality_var.get()
    output_format = format_var.get()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira a URL do vídeo.")
        return
    download_youtube_video(url, quality, output_format, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list, downloaded_files_frame)
    url_entry.delete(0, tk.END)

def create_gui():
    root = tk.Tk()
    root.title("BaixaTube By Vic")
    root.iconbitmap('assets/icone.ico')

    pygame.mixer.init()

    create_menu(root, open_download_directory)

    tk.Label(root, text="URL do vídeo do YouTube:").grid(row=0, column=0, padx=10, pady=5)
    url_entry = tk.Entry(root, width=50)
    url_entry.grid(row=0, column=1, padx=10, pady=5)
    download_button = tk.Button(root, text="Baixar", bg="blue", fg="white", width=10, command=lambda: start_download(
        url_entry, quality_var, format_var, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list, downloaded_files_frame))
    download_button.grid(row=0, column=2, padx=10, pady=5)

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

    # Ajustar Título dos Arquivos Baixados e Botão Abrir Diretório
    title_frame = tk.Frame(root)
    title_frame.grid(row=9, column=0, columnspan=3, sticky='ew', padx=10, pady=5)
    title_label = tk.Label(title_frame, text="Arquivos já baixados:", font=('Helvetica', 12, 'bold'))
    title_label.pack(side='left')
    open_directory_button = tk.Button(title_frame, text="Abrir diretório de downloads", bg="orange", fg="white", command=open_download_directory)
    open_directory_button.pack(side='right')
