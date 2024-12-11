import os
import tkinter as tk
from tkinter import messagebox, ttk
import pygame
from .menu import create_menu
from .dialogs import open_download_directory
from .list_utils import update_downloaded_files_list
from .url_section import create_url_section
from .download_options import create_download_options
from .progress_section import create_progress_section
from src.downloader import download_youtube_video

def start_download(url_entry, quality_var, format_var, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list, downloaded_files_frame, message_label):
    print("Iniciando download")  # Log para verificar o início do download
    url = url_entry.get()
    quality = quality_var.get()
    output_format = format_var.get()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira a URL do vídeo.")
        return
    download_youtube_video(url, quality, output_format, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list, downloaded_files_frame, message_label)
    url_entry.delete(0, tk.END)

def create_gui():
    root = tk.Tk()
    root.title("BaixaTube By Vic")
    root.iconbitmap('assets/icone.ico')

    pygame.mixer.init()

    create_menu(root, open_download_directory)

    # Seção de URL
    url_entry = tk.Entry(root)
    url_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=2, sticky="ew")
    quality_var = tk.StringVar()
    format_var = tk.StringVar()

    # Campo de Mensagens
    message_label = tk.Label(root, text="", fg="blue")
    message_label.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

    create_url_section(root, start_download, url_entry, quality_var, format_var, ttk.Progressbar(root), tk.Label(root), tk.StringVar(), messagebox, update_downloaded_files_list, tk.Frame(root), message_label)

    # Opções de Download
    create_download_options(root, quality_var, format_var)

    # Barra de Progresso
    progress_bar = ttk.Progressbar(root)
    status_label = tk.Label(root)
    progress = tk.StringVar()
    create_progress_section(root, progress_bar, status_label, progress)

    # Ajustar Título dos Arquivos Baixados e Botão Abrir Diretório
    title_frame = tk.Frame(root)
    title_frame.grid(row=9, column=0, columnspan=3, sticky='ew', padx=10, pady=5)
    title_label = tk.Label(title_frame, text="Arquivos já baixados:", font=('Helvetica', 12, 'bold'))
    title_label.pack(side='left')
    open_directory_button = tk.Button(title_frame, text="Abrir diretório de downloads", bg="orange", fg="white", command=open_download_directory)
    open_directory_button.pack(side='left')  # Alinhado à esquerda para colocar botão de atualizar ao lado

    # Botão de Atualização Manual
    update_button = tk.Button(title_frame, text="Atualizar Lista", bg="green", fg="white", command=lambda: update_downloaded_files_list(os.path.join(os.getcwd(), 'downloads'), scrollable_frame, root))
    update_button.pack(side='right')

    # Adicionando uma linha abaixo do título
    title_separator = tk.Frame(root, height=2, bd=1, relief="sunken")
    title_separator.grid(row=10, column=0, columnspan=3, sticky='ew', padx=10, pady=5)

    downloaded_files_frame = tk.Frame(root)
    downloaded_files_frame.grid(row=11, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')

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

    update_downloaded_files_list(os.path.join(os.getcwd(), 'downloads'), scrollable_frame, root)

    root.mainloop()
