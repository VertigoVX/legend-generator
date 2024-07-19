import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import time

# List of valid regions in Uganda
valid_regions = [
    'Central', 'Eastern', 'Northern', 'Western', 'Kampala', 'Wakiso',
    'Mukono', 'Mbarara', 'Gulu', 'Lira', 'Jinja', 'Mbale', 'Fort Portal', 'Soroti'
]


def create_legend_image(labels, colors, output_path, logo_path, region, bounding_box, logo_scale=0.5):
    """
    Creates a legend image with the specified labels and colors, including a logo, region, timestamp, and bounding box.

    :param labels: List of labels for the legend.
    :param colors: List of colors corresponding to the labels.
    :param output_path: File path to save the legend image.
    :param logo_path: File path to the logo image.
    :param region: Name of the region.
    :param bounding_box: Bounding box coordinates.
    :param logo_scale: Scaling factor for the logo size.
    """
    # Ensure the number of labels matches the number of colors
    assert len(labels) == len(colors), "Labels and colors must have the same length"

    # Load and resize the logo image
    try:
        logo = Image.open(logo_path)
        logo_width, logo_height = logo.size
        logo = logo.resize((int(logo_width * logo_scale), int(logo_height * logo_scale)), Image.LANCZOS)
        logo = np.array(logo)
    except Exception as e:
        print(f"Error loading logo: {e}")
        return

    # Create a smaller figure and a subplot
    fig, ax = plt.subplots(figsize=(4, 5))  # Adjust the figure size to be more compact
    fig.patch.set_visible(False)
    ax.axis('off')

    # Add the logo using imshow
    ax_logo = fig.add_axes([0.1, 0.7, 0.3, 0.2], anchor='NW', zorder=1)
    ax_logo.imshow(logo)
    ax_logo.axis('off')

    # Add the legend
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10)
               for color in colors]
    ax.legend(handles, labels, loc='center', frameon=False, fontsize=10, bbox_to_anchor=(0.5, 0.4))

    # Add the region name above the timestamp
    plt.text(0.5, 0.25, f'Region: {region}', ha='center', va='center', transform=fig.transFigure, fontsize=12)

    # Add the bounding box coordinates
    plt.text(0.5, 0.18, f'Bounding Box Coordinates: {bounding_box}', ha='center', va='center',
             transform=fig.transFigure, fontsize=10)

    # Add the date and time
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    plt.text(0.5, 0.1, f'Generated on: {timestamp}', ha='center', va='center', transform=fig.transFigure, fontsize=10)

    # Save the legend as an image
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()  # Close the plot to free up memory


def browse_file():
    filename = filedialog.askopenfilename()
    return filename


def get_valid_region():
    while True:
        region = simpledialog.askstring("Input", "Enter the region where the plot is taking place:")
        if region is None:
            messagebox.showerror("Error", "Region not specified")
            continue
        if region in valid_regions:
            return region
        else:
            messagebox.showerror("Error", "Invalid region. Please enter a valid region in Uganda.")


def get_valid_bounding_box():
    while True:
        bounding_box = simpledialog.askstring("Input",
                                              "Enter the bounding box coordinates (format: xmin, ymin, xmax, ymax):")
        if bounding_box is None:
            messagebox.showerror("Error", "Bounding box coordinates not specified")
            continue
        try:
            coords = list(map(float, bounding_box.split(',')))
            if len(coords) != 4:
                raise ValueError("There must be exactly 4 values.")
            xmin, ymin, xmax, ymax = coords
            if xmin >= xmax or ymin >= ymax:
                raise ValueError("Max values cannot be lower than or equal to min values.")
            return f"{xmin}, {ymin}, {xmax}, {ymax}"
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid bounding box coordinates: {e}")


def main():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Create and display the splash screen
    splash_root = tk.Toplevel()
    splash_root.overrideredirect(True)  # Remove window decorations (title bar, borders, etc.)
    splash_root.geometry("300x200+500+300")  # Set the window size and position

    splash_label = tk.Label(splash_root, text="Loading...", font=("Helvetica", 18))
    splash_label.pack(expand=True)

    # Update the splash screen before proceeding
    splash_root.update()

    # Simulate loading time (you can replace this with actual loading logic)
    time.sleep(2)

    # Hide the splash screen after loading is complete
    splash_root.destroy()

    logo_path = browse_file()
    if not logo_path:
        messagebox.showerror("Error", "Logo file not selected")
        return

    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if not output_path:
        messagebox.showerror("Error", "Output path not specified")
        return

    region = get_valid_region()

    bounding_box = get_valid_bounding_box()

    labels = ['Roads', 'Wire', 'Meters', 'Composite Switch MV', 'Distribution Transformer', 'Pole Structure']
    colors = ['red', 'blue', 'black', 'green', 'purple', 'yellow']

    create_legend_image(labels, colors, output_path, logo_path, region, bounding_box)
    messagebox.showinfo("Success", f"Legend image created successfully at {output_path}")


if __name__ == "__main__":
    main()
