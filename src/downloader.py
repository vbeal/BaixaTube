import yt_dlp
import os
from src.utils import strip_ansi_codes
from src.gui.list_utils import update_downloaded_files_list
from src.gui.dialogs import play_click_sound

def download_progress_hook(d, progress_bar, status_label, progress, messagebox, root, downloaded_files_frame, message_label):
    print("Hook de progresso chamado")  # Log para verificar se a função é chamada
    if d['status'] == 'downloading':
        print("Status: Baixando")  # Log para verificar o status do download
        p = strip_ansi_codes(d['_percent_str']).strip()
        speed = strip_ansi_codes(d['_speed_str']).strip()
        remaining = strip_ansi_codes(d['_eta_str']).strip()
        total_size = strip_ansi_codes(d.get('_total_bytes_str', '')).strip() or strip_ansi_codes(d.get('_total_bytes_estimate_str', '')).strip()

        try:
            message = f"{p} of {total_size} at {speed}, faltam {remaining}"
            message_label.config(text=message)
            progress_bar['value'] = float(p.strip('%'))
            root.update_idletasks()  # Atualiza a interface gráfica
            print(f"Progresso: {message}")  # Log para verificar a mensagem
        except ValueError as e:
            print(f"Erro ao converter string para float: {e}")
            message_label.config(text="Erro na atualização do progresso")

    if d['status'] == 'finished':
        print("Status: Concluído")  # Log para verificar o status do download
        message_label.config(text="Download concluído")
        progress_bar['value'] = 100
        status_label.config(text="Pronto! 100%")
        messagebox.showinfo("Sucesso", "Download concluído!")
        play_click_sound()
        update_downloaded_files_list(os.path.join(os.getcwd(), 'downloads'), downloaded_files_frame, root)
        root.update()  # Força a atualização da interface gráfica
        root.after(5000, lambda: reset_download_ui(progress_bar, status_label, progress, root))

def reset_download_ui(progress_bar, status_label, progress, root):
    progress_bar['value'] = 0
    status_label.config(text="")
    progress.set("")
    root.update_idletasks()  # Atualiza a interface gráfica

def download_youtube_video(url, quality, output_format, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list, downloaded_files_frame, message_label):
    save_path = os.path.join(os.getcwd(), 'downloads')
    print(f"Diretório de salvamento: {save_path}")  # Log para verificar o caminho do diretório
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    ydl_opts = {
        'format': quality,
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: download_progress_hook(d, progress_bar, status_label, progress, messagebox, root, downloaded_files_frame, message_label)],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if output_format == 'mp3' else [],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        update_downloaded_files_list(save_path, downloaded_files_frame, root)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
