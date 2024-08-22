import tkinter as tk
import subprocess
import os

def open_detection_window():
    # Adjust the path to match your detection script location
    detection_script_path = r'C:\Users\kulka\PycharmProjects\SignLingo\interference classifier.py'
    subprocess.Popen(["python", detection_script_path], shell=True)

root = tk.Tk()
root.title("Main Window")

# Create a button that opens the detection window
button = tk.Button(root, text="Open Detection Window", command=open_detection_window)
button.pack(pady=20)

root.mainloop()
