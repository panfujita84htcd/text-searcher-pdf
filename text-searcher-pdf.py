import os
import tkinter as tk
from tkinter import filedialog, scrolledtext

from PyPDF2 import PdfReader
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.environ['TCL_LIBRARY'] = os.path.join(sys._MEIPASS, 'tcl')
    os.environ['TK_LIBRARY'] = os.path.join(sys._MEIPASS, 'tk')


def search_pdf_files(folder_path, search_string):
    results.delete(1.0, tk.END)  # Clear the results text widget
    search_string_lower = search_string.lower()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.pdf'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as f:
                        pdf = PdfReader(f)
                        num_pages = len(pdf.pages)
                        for page_num in range(num_pages):
                            page = pdf.pages[page_num]
                            text = page.extract_text()
                            text_lower = text.lower()
                            if search_string_lower in text_lower:
                                result_text = f"Found '{search_string}' in {file_path} on page {page_num + 1}\n"
                                results.insert(tk.END, result_text)
                except Exception as e:
                    error_text = f"Error reading {file_path}: {e}\n"
                    results.insert(tk.END, error_text)


def browse_folder():
    folder_path = filedialog.askdirectory()
    folder_var.set(folder_path)


def start_search():
    folder_path = folder_var.get()
    search_string = search_var.get()
    status_label.config(text="Searching... It can take minutes.")
    root.update_idletasks()
    search_pdf_files(folder_path, search_string)
    status_label.config(text="Search completed.")


root = tk.Tk()
root.title("PDF Search")

folder_var = tk.StringVar()
search_var = tk.StringVar()

folder_label = tk.Label(root, text="Folder:")
folder_label.grid(row=0, column=0, sticky="e")

folder_entry = tk.Entry(root, textvariable=folder_var, width=50)
folder_entry.grid(row=0, column=1)

browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=0, column=2)

search_label = tk.Label(root, text="Search String:")
search_label.grid(row=1, column=0, sticky="e")

search_entry = tk.Entry(root, textvariable=search_var, width=50)
search_entry.grid(row=1, column=1)

start_button = tk.Button(root, text="Start Search", command=start_search)
start_button.grid(row=2, column=1, pady=10)

results_label = tk.Label(root, text="Results:")
results_label.grid(row=3, column=0, sticky="nw")

results = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=10)
results.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

status_label = tk.Label(root, text="")
status_label.grid(row=5, column=0, columnspan=3, sticky="w")

root.mainloop()

