import tkinter as tk

def create_download_options(root, quality_var, format_var):
    options_frame = tk.LabelFrame(root, text="Opções de Download", padx=10, pady=10)
    options_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky='ew')

    tk.Label(options_frame, text="Qualidade:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    quality_var.set("worst")  # Padrão: Média qualidade
    tk.Radiobutton(options_frame, text="Alta qualidade (best)", variable=quality_var, value="best").grid(row=0, column=1, padx=10, pady=5, sticky='w')
    tk.Radiobutton(options_frame, text="Média qualidade (worst)", variable=quality_var, value="worst").grid(row=1, column=1, padx=10, pady=5, sticky='w')
    tk.Radiobutton(options_frame, text="Somente áudio (bestaudio)", variable=quality_var, value="bestaudio").grid(row=2, column=1, padx=10, pady=5, sticky='w')

    tk.Label(options_frame, text="Formato:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
    format_var.set("mp4")
    tk.Radiobutton(options_frame, text="MP4", variable=format_var, value="mp4").grid(row=3, column=1, padx=10, pady=5, sticky='w')
    tk.Radiobutton(options_frame, text="MP3", variable=format_var, value="mp3").grid(row=4, column=1, padx=10, pady=5, sticky='w')
