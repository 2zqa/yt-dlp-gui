import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from yt_dlp import YoutubeDL

def main():
    def on_download():
        text = entry.get()
        if not text.startswith(('https://www.youtube.com/', 'https://youtu.be/', 'http://www.youtube.com/')):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return

        progress_bar['value'] = 0
        thread = threading.Thread(target=lambda: download(text))
        thread.daemon = True
        thread.start()

    def download(text: str):
        ydl_opts = {
            'progress_hooks': [progress_hook],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([text])

    def progress_hook(d):
        if d['status'] == 'downloading':
            percent = (float(d['downloaded_bytes']) / float(d['total_bytes'])) * 100
            window.after(0, update_progress, percent)
        elif d['status'] == 'finished':
            window.after(0, update_progress, 100)

    def update_progress(percentage: float):
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

    # Create and position the button
    button = tk.Button(frame, text="Download", command=on_download)
    button.grid(row=0, column=1, padx=10, pady=10)

    # Create and position the progress bar
    progress_bar = ttk.Progressbar(frame, length=300, mode='determinate')
    progress_bar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Start the GUI event loop
    window.mainloop()


if __name__ == "__main__":
    main()
