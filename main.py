import matplotlib.pyplot as plt
import numpy as np
import json
import os
import tkinter as tk
from tkinter import messagebox
from matplotlib.patches import Ellipse, Circle
from matplotlib.animation import FuncAnimation


def save_data(energy, transport, diet, footprint_score):
    data = {'energy': energy, 'transport': transport, 'diet': diet, 'footprint_score': footprint_score}
    file_path = "carbon_footprint_data.json"

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            history = json.load(file)
    else:
        history = []

    history.append(data)
    with open(file_path, 'w') as file:
        json.dump(history, file, indent=4)


def draw_footprint(ax, x, y, size, color):
    sole = Ellipse((x, y), width=size * 1.5, height=size * 2.5, color=color, alpha=0.7)
    ax.add_patch(sole)

    toe_offsets = [(0, size * 1.5), (-size * 0.5, size * 1.6), (size * 0.5, size * 1.6), (-size * 0.3, size * 2),
                   (size * 0.3, size * 2)]
    for dx, dy in toe_offsets:
        toe = Circle((x + dx, y + dy), size * 0.3, color=color, alpha=0.7)
        ax.add_patch(toe)


def animate_footprint(footprint_score, color):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    size = max(min(footprint_score / 100, 0.5), 0.2)
    x_positions = np.linspace(1, 9, 5)
    y_position = 1.5

    def update(frame):
        draw_footprint(ax, x_positions[frame], y_position, size, color)
        return ax.patches

    ani = FuncAnimation(fig, update, frames=len(x_positions), interval=500, repeat=False)
    plt.show()


def calculate_footprint():
    try:
        energy = int(energy_entry.get())
        transport = int(transport_entry.get())
        diet = int(diet_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter numeric values.")
        return

    footprint_score = (energy * 0.5) + (transport * 0.3) + (diet * 2)

    if footprint_score < 100:
        color = 'green'
        result_text.set("Your carbon consumption is LOW.")
    elif footprint_score < 300:
        color = 'yellow'
        result_text.set("Your carbon consumption is MODERATE.")
    else:
        color = 'red'
        result_text.set("Your carbon consumption is HIGH.")

    save_data(energy, transport, diet, footprint_score)
    animate_footprint(footprint_score, color)


# Create GUI
root = tk.Tk()
root.title("Carbon Footprint Calculator")

tk.Label(root, text="Enter your energy consumption (kWh/month):").pack()
energy_entry = tk.Entry(root)
energy_entry.pack()

tk.Label(root, text="Enter your transport usage (miles/week):").pack()
transport_entry = tk.Entry(root)
transport_entry.pack()

tk.Label(root, text="How many plants have you planted this week?").pack()
diet_entry = tk.Entry(root)
diet_entry.pack()

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, fg="blue").pack()

tk.Button(root, text="Calculate Footprint", command=calculate_footprint).pack()
root.mainloop()
