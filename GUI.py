import tkinter as tk
from SpeedTracker import *

# Create the main window
root = tk.Tk()


def start_function():
    Speed_Tracker()


def stop_function():
    pass


root.title("Object Tracking System")

root.geometry("800x480")
root.configure(bg="#00072D")

# Calculate coordinates to place the button in the center
button_width = 12
button_height = 3
window_width = root.winfo_reqwidth()  # Get the window width
window_height = root.winfo_reqheight()  # Get the window height
x_pos = (window_width - button_width) / 2  # Calculate x-coordinate
y_pos = (window_height - button_height) / 2  # Calculate y-coordinate

frame = tk.Frame(root, bg="#7289DA")  # Use the same background color as the window
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Function to be called when the button is clicked
start_button = tk.Button(frame, text="Start", command=start_function, width=button_width, height=button_height)
start_button.pack()

# Stop button
stop_button = tk.Button(frame, text="Stop", command=stop_function, width=button_width, height=button_height)
stop_button.pack()

# Run the main loop
root.mainloop()
