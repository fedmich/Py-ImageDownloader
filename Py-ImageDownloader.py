import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os
import platform

def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_data = response.content
        return img_data
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def convert_image_to_png(image_data, save_path):
    try:
        img = Image.open(BytesIO(image_data))
        img = img.convert("RGBA")  # Ensure the image is in a suitable format
        img.save(save_path, "PNG", quality=97)
        return save_path
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            break
        size /= 1024
    return f"{size:.{decimal_places}f} {unit}"

def go_button_click():
    url = url_entry.get()
    save_path = filepath_entry.get()
    
    if not url or not save_path:
        messagebox.showwarning("Input Error", "Please provide both URL and file path.")
        return
    
    progress_bar.start()
    status_label.config(text="Downloading...")
    root.update_idletasks()  # Force update to show status text immediately
    
    img_data = download_image(url)
    progress_bar.stop()
    
    if img_data:
        status_label.config(text="Converting to PNG...")
        root.update_idletasks()  # Force update to show status text immediately
        saved_file = convert_image_to_png(img_data, save_path)
        if saved_file:
            status_label.config(text="Done")
            update_image_preview(saved_file)

def browse_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if platform.system() == "Windows":
        file_path = file_path.replace('/', '\\')
    filepath_entry.delete(0, tk.END)
    filepath_entry.insert(0, file_path)

def update_image_preview(file_path):
    try:
        img = Image.open(file_path)
        img.thumbnail((300, 300))
        img_preview = ImageTk.PhotoImage(img)
        image_label.config(image=img_preview)
        image_label.image = img_preview

        file_size = os.path.getsize(file_path)
        file_info_label.config(text=f"File size: {human_readable_size(file_size)}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Image Downloader")
root.geometry("500x600")

tk.Label(root, text="URL:").grid(row=0, column=0, sticky=tk.W)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

tk.Label(root, text="Save Path:").grid(row=1, column=0, sticky=tk.W)
filepath_entry = tk.Entry(root, width=40)
filepath_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_file).grid(row=1, column=2, padx=5, pady=5)

tk.Button(root, text="GO", command=go_button_click).grid(row=2, column=0, columnspan=3, pady=10)

status_frame = tk.Frame(root)
status_frame.grid(row=3, column=0, columnspan=3, pady=5)

progress_bar = Progressbar(status_frame, mode='indeterminate')
progress_bar.pack(side=tk.LEFT, padx=5)
status_label = tk.Label(status_frame, text="", font=("Helvetica", 16))
status_label.pack(side=tk.LEFT, padx=5)

file_info_label = tk.Label(root, text="")
file_info_label.grid(row=4, column=0, columnspan=3, pady=5)

image_label = tk.Label(root)
image_label.grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()
