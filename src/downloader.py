import yt_dlp
import os
from .utils import strip_ansi_codes

def download_progress_hook(d, progress_bar, status_label, progress, messagebox, root):
    """
    Hook para monitorar o progresso do download e atualizar a interface gráfica.

    Parâmetros:
        d (dict): Dicionário de dados de progresso do yt-dlp.
        progress_bar (ttk.Progressbar): Barra de progresso da GUI.
        status_label (tk.Label): Rótulo para mostrar o status do download.
        progress (tk.StringVar): Variável para texto de progresso.
        messagebox (tk.Messagebox): Caixa de mensagem da GUI.
        root (tk.Tk): Instância principal da GUI.
    """
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
        root.after(5000, lambda: reset_download_ui(progress_bar, status_label, progress, root))

def reset_download_ui(progress_bar, status_label, progress, root):
    """
    Reseta os elementos da interface gráfica após a conclusão do download.

    Parâmetros:
        progress_bar (ttk.Progressbar): Barra de progresso da GUI.
        status_label (tk.Label): Rótulo para mostrar o status do download.
        progress (tk.StringVar): Variável para texto de progresso.
        root (tk.Tk): Instância principal da GUI.
    """
    progress_bar['value'] = 0
    status_label.config(text="")
    progress.set("")

def download_youtube_video(url, quality, output_format, progress_bar, status_label, progress, messagebox, root, update_downloaded_files_list):
    """
    Faz o download de um vídeo do YouTube usando yt-dlp.

    Parâmetros:
        url (str): URL do vídeo do YouTube.
        quality (str): Qualidade do vídeo.
        output_format (str): Formato de saída do arquivo.
        progress_bar (ttk.Progressbar): Barra de progresso da GUI.
        status_label (tk.Label): Rótulo para mostrar o status do download.
        progress (tk.StringVar): Variável para texto de progresso.
        messagebox (tk.Messagebox): Caixa de mensagem da GUI.
        root (tk.Tk): Instância principal da GUI.
        update_downloaded_files_list (function): Função para atualizar a lista de arquivos baixados.
    """
    save_path = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    ydl_opts = {
        'format': quality,
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: download_progress_hook(d, progress_bar, status_label, progress, messagebox, root)],
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if output_format == 'mp3' else [],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        update_downloaded_files_list(save_path)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
