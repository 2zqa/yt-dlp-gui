import tkinter as tk
from tkinter import messagebox


def main():
    def button_click():
        text = entry.get()
        messagebox.showinfo("Input", f"You entered: {text}")

    window = tk.Tk()
    window.title("Text Input Example")

    # Create and position the entry field
    entry = tk.Entry(window)
    entry.grid(row=0, column=0, padx=10, pady=10)

    # Create and position the button
    button = tk.Button(window, text="Submit", command=button_click)
    button.grid(row=0, column=1, padx=10, pady=10)

    # Start the GUI event loop
    window.mainloop()


if __name__ == "__main__":
    main()
