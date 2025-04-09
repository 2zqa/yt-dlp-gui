import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from yt_dlp import YoutubeDL
from datetime import datetime
import logging

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    logger = logging.getLogger(__name__)

    def on_download():
        text = entry.get()
        if not text.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'http://www.youtube.com/')):
            logger.error(f"Invalid URL attempted: {text}")
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return

        progress_bar['value'] = 0
        status_label.config(text=f"In progress... Started @ {datetime.now().strftime('%H:%M:%S')}")
        logger.info(f"Starting download for URL: {text}")
        thread = threading.Thread(target=lambda: download(text))
        thread.daemon = True
        thread.start()

    def download(text: str):
        try:
            ydl_opts = {
                'progress_hooks': [progress_hook],
                'logger': logger,
                'format': 'm4a/bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }]
            }
            with YoutubeDL(ydl_opts) as ydl:
                logger.info("Initializing YoutubeDL")
                ydl.download([text])
        except Exception as e:
            logger.error(f"Download failed: {str(e)}")
            messagebox.showerror("Error", f"Download failed: {str(e)}")

    def progress_hook(d: dict[str, str]) -> None:
        if d['status'] == 'downloading':
            percent = (float(d['downloaded_bytes']) / float(d['total_bytes'])) * 100
            logger.debug(f"Download progress: {percent:.2f}%")
            window.after(0, update_progress, percent)
        elif d['status'] == 'finished':
            logger.info("Download completed successfully")
            window.after(0, update_progress, 100)
            window.after(0, lambda: status_label.config(text=f"Finished @ {datetime.now().strftime('%H:%M:%S')}"))

    def update_progress(percentage: float) -> None:
        progress_bar['value'] = percentage

    window = tk.Tk()
    window.title("yt-dlp GUI")
    window.geometry("800x400")

    logger.info("Starting application")

    # Create a container frame and center it
    frame = tk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor='center')

    # Create and position the entry field
    entry = tk.Entry(frame)
    entry.grid(row=0, column=0, padx=10, pady=10)

    # Create and position the button
    button = tk.Button(frame, text="Download", command=on_download)
    button.grid(row=0, column=1, padx=10, pady=10)

    # Create and position the progress bar
    progress_bar = ttk.Progressbar(frame, length=300, mode='determinate')
    progress_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Create and position the status label
    status_label = tk.Label(frame, text="Waiting for download...")
    status_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Start the GUI event loop
    window.mainloop()

if __name__ == "__main__":
    main()
