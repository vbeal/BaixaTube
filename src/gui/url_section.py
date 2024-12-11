import tkinter as tk

def create_url_section(root, start_download, url_entry, quality_var, format_var, progress_bar, status_label, progress, messagebox, update_downloaded_files_list, downloaded_files_frame, message_label):
    url_label = tk.Label(root, text="URL do vídeo:")
    url_label.grid(row=0, column=0, padx=10, pady=5)

    url_entry.grid(row=0, column=1, padx=10, pady=5, columnspan=2, sticky="ew")

    download_button = tk.Button(root, text="Baixar", bg="blue", fg="white", width=10, command=lambda: start_download(
        url_entry, quality_var, format_var, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list, downloaded_files_frame, message_label))
    download_button.grid(row=0, column=3, padx=10, pady=5)
