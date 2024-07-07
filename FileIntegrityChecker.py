#Noor Nihay



import hashlib
import os
import json
import argparse
import tkinter as tk
from tkinter import filedialog, messagebox

def calculate_checksum(file_path, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def store_checksums(directory, output_file='checksums.json', algorithm='sha256'):
    checksums = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            checksums[file_path] = calculate_checksum(file_path, algorithm)

    with open(output_file, 'w') as f:
        json.dump(checksums, f, indent=4)

    messagebox.showinfo("Success", f"Checksums stored in {output_file}")

def verify_checksums(checksum_file='checksums.json', algorithm='sha256'):
    if not os.path.exists(checksum_file):
        messagebox.showerror("Error", f"Checksum file {checksum_file} not found.")
        return

    with open(checksum_file, 'r') as f:
        stored_checksums = json.load(f)

    mismatches = []
    for file_path, stored_checksum in stored_checksums.items():
        if os.path.exists(file_path):
            current_checksum = calculate_checksum(file_path, algorithm)
            if current_checksum != stored_checksum:
                mismatches.append(file_path)
        else:
            mismatches.append(file_path)

    if mismatches:
        messagebox.showwarning("Warning", f"Checksum mismatches or missing files:\n\n" + "\n".join(mismatches))
    else:
        messagebox.showinfo("Success", "All files verified successfully.")

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

def store_action():
    directory = directory_entry.get()
    if directory:
        store_checksums(directory)
    else:
        messagebox.showerror("Error", "Please select a directory.")

def verify_action():
    checksum_file = checksum_file_entry.get()
    if checksum_file:
        verify_checksums(checksum_file)
    else:
        messagebox.showerror("Error", "Please select a checksum file.")

#Set up for the GUI
root = tk.Tk()
root.title("File Integrity Checker")
#Noor Nihay
# Select Directory for GUI
directory_label = tk.Label(root, text="Directory:")
directory_label.grid(row=0, column=0, padx=5, pady=5)

directory_entry = tk.Entry(root, width=50)
directory_entry.grid(row=0, column=1, padx=5, pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.grid(row=0, column=2, padx=5, pady=5)

# Store checksums button
store_button = tk.Button(root, text="Store Checksums", command=store_action)
store_button.grid(row=1, column=0, columnspan=3, pady=10)
#Noor Nihay

#Checksum file selection (Select a file within a directory)
checksum_file_label = tk.Label(root, text="Checksum File:")
checksum_file_label.grid(row=2, column=0, padx=5, pady=5)

checksum_file_entry = tk.Entry(root, width=50)
checksum_file_entry.grid(row=2, column=1, padx=5, pady=5)

checksum_browse_button = tk.Button(root, text="Browse", command=lambda: checksum_file_entry.insert(0, filedialog.askopenfilename()))
checksum_browse_button.grid(row=2, column=2, padx=5, pady=5)

# Verifying files (Input button)
verify_button = tk.Button(root, text="Verify Checksums", command=verify_action)
verify_button.grid(row=3, column=0, columnspan=3, pady=10)

root.mainloop()
