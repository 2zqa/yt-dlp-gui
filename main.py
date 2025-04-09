import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from yt_dlp import YoutubeDL
from datetime import datetime
import logging

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting application")

    def on_download() -> None:
        text = entry.get()
        if not text.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'http://www.youtube.com/')):
            logger.error(f"Invalid URL attempted: {text}")
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return

        progress_bar['value'] = 0
        status_label.config(text=f"In progress... Started on {datetime.now().strftime('%H:%M')}")
        logger.info(f"Starting download for URL: {text}")
        thread = threading.Thread(target=lambda: download(text))
        thread.daemon = True
        thread.start()

    def download(url: str) -> None:
        logger.info("Starting download")
        ydl_opts = {
            'progress_hooks': [progress_hook],
            'logger': logger,
            'format': 'm4a/bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(url)
        except Exception as e:
            logger.error(f"Download failed: {str(e)}")
            messagebox.showerror("Error", f"Download failed: {str(e)}")

        window.after(0, lambda: status_label.config(text=f"Finished at {datetime.now().strftime('%H:%M')}"))

    def progress_hook(d: dict[str, str]) -> None:
        if d['status'] == 'downloading':
            percent = (float(d['downloaded_bytes']) / float(d['total_bytes'])) * 100
            logger.debug(f"Download progress: {percent:.2f}%")
            window.after(0, update_progress, percent)
        elif d['status'] == 'finished':
            logger.info("Download completed successfully")
            window.after(0, update_progress, 100)

    def update_progress(percentage: float) -> None:
        progress_bar['value'] = percentage

    window = tk.Tk()
    window.title("yt-dlp GUI")
    window.geometry("800x400")

    # Create a container frame and center it
    frame = tk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    # Create and position the entry field
    entry = tk.Entry(frame)
    entry.grid(row=0, column=0, padx=10, pady=10)

    button = tk.Button(frame, text="Download", command=on_download)
    button.grid(row=0, column=1, padx=10, pady=10)

    status_label = tk.Label(window, text="Not started")
    status_label.place(relx=0.02, rely=0.90, anchor='sw')

    progress_bar = ttk.Progressbar(window, mode='determinate')
    progress_bar.place(relx=0.02, rely=0.92, relwidth=0.96, height=20)

    # Start the GUI event loop
    window.mainloop()
    logger.info("Application exited")

if __name__ == "__main__":
    main()
