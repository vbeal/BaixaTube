import os
from tkinter import messagebox
import pygame  # Adicione esta linha para importar o pygame

def open_file(path):
    os.startfile(path)

def open_download_directory():
    save_path = os.path.join(os.getcwd(), 'downloads')
    if os.path.exists(save_path):
        os.startfile(save_path)
    else:
        messagebox.showwarning("Aviso", "O diretório de downloads não existe.")

def play_click_sound():
    pygame.mixer.Sound('assets/click.wav').play()
