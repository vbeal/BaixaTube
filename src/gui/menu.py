import tkinter as tk

def create_menu(root, open_download_directory):
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Abrir diretório de downloads", command=open_download_directory)
    file_menu.add_command(label="Sair", command=root.quit)
    menu_bar.add_cascade(label="Arquivo", menu=file_menu)
    root.config(menu=menu_bar)
