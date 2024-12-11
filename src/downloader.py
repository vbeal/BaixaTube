import yt_dlp
import os
from src.utils import strip_ansi_codes
from src.gui.download_list import update_downloaded_files_list
from src.gui.dialogs import play_click_sound

def download_progress_hook(d, progress_bar, status_label, progress, messagebox, root, downloaded_files_frame):
    if d['status'] == 'downloading':
        p = strip_ansi_codes(d['_percent_str']).strip()
        speed = strip_ansi_codes(d['_speed_str']).strip()
        remaining = strip_ansi_codes(d['_eta_str']).strip()

        try:
            progress.set(f"Baixando: {p} a {speed}, faltam {remaining}")
            progress_bar['value'] = float(p.strip('%'))
            if float(p.strip('%')) < 50:
                status_label.config(text="Oba! Iniciando o download...")
            elif float(p.strip('%')) < 80:
                status_label.config(text="Estamos já no meio, quase pronto...")
            else:
                status_label.config(text="Finalizando e...")
        except ValueError as e:
            print(f"Erro ao converter string para float: {e}")
            progress.set("Erro na atualização do progresso")

    if d['status'] == 'finished':
        progress.set("Download concluído")
        progress_bar['value'] = 100
        status_label.config(text="Pronto! 100%")
        messagebox.showinfo("Sucesso", "Download concluído!")
        play_click_sound()
        root.after(5000, lambda: reset_download_ui(progress_bar, status_label, progress, root))

def reset_download_ui(progress_bar, status_label, progress, root):
    progress_bar['value'] = 0
    status_label.config(text="")
    progress.set("")

def download_youtube_video(url, quality, output_format, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list, downloaded_files_frame):
    save_path = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    ydl_opts = {
        'format': quality,
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: download_progress_hook(d, progress_bar, status_label, progress, messagebox, root, downloaded_files_frame)],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if output_format == 'mp3' else [],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        update_downloaded_files_list(save_path, downloaded_files_frame)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
