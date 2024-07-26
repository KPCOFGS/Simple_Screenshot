import tkinter as tk
from tkinter import Canvas, Button, filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab
import os
import time
import json

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot App")
        self.root.geometry("400x300")  # Width x Height
        # Load settings
        self.settings_file = "settings.json"
        self.load_settings()

        # Create widgets for settings
        self.create_widgets()

        # Center the window on the screen
        self.center_window(self.root)

        # Initialize preview window as None
        self.preview_window = None

    def create_widgets(self):


        tk.Button(self.root, text="Select Directory to Save", command=self.select_directory).pack(pady=5)
        tk.Label(self.root, text="(Automatically saves the path)").pack(pady=5)
        tk.Label(self.root, text="Delay in seconds:").pack(pady=5)
        self.delay_entry = tk.Entry(self.root, width=10)
        self.delay_entry.insert(0, str(self.delay))
        self.delay_entry.pack(pady=5)

        tk.Button(self.root, text="Start Capturing", command=self.start_capturing).pack(pady=20)

        # Button to take a full screenshot
        tk.Button(self.root, text="Take Full Screenshot", command=self.take_full_screenshot).pack(pady=20)

    def center_window(self, window):
        window.update_idletasks()  # Update window to get the correct size
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def select_directory(self):
        new_directory = filedialog.askdirectory()
        if new_directory:  # Check if a valid directory was selected
            self.save_directory = new_directory
            self.save_settings()

    def start_capturing(self):
        try:
            self.delay = int(self.delay_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Delay must be an integer.")
            return
        if self.delay < 0:
            messagebox.showerror("Invalid Input", "Delay cannot be negative")
            return
        # Destroy preview window if it is open
        if self.preview_window and self.preview_window.winfo_exists():
            self.preview_window.destroy()
            self.preview_window = None

        self.save_settings()

        # Close the settings window
        self.root.withdraw()

        # Apply delay
        time.sleep(self.delay)
        time.sleep(0.1)
        # Take full-screen screenshot
        self.screenshot = ImageGrab.grab()

        # Show the screenshot in fullscreen mode
        self.show_fullscreen_image()

    def take_full_screenshot(self):
        try:
            self.delay = int(self.delay_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Delay must be an integer.")
            return
        if self.delay < 0:
            messagebox.showerror("Invalid Input", "Delay cannot be negative")
            return

        # Destroy preview window if it is open
        if self.preview_window and self.preview_window.winfo_exists():
            self.preview_window.destroy()
            self.preview_window = None

        self.save_settings()

        # Hide the main window
        self.root.withdraw()

        # Apply delay
        time.sleep(self.delay)
        time.sleep(0.1)

        # Take full-screen screenshot
        self.screenshot = ImageGrab.grab()

        # Show the main window again
        self.root.deiconify()

        # Set the selected region to cover the entire screenshot
        self.selected_region = (0, 0, self.screenshot.width, self.screenshot.height)

        # Show preview of the screenshot
        self.show_preview()
    def show_fullscreen_image(self):
        self.fullscreen_window = tk.Toplevel(self.root)
        self.fullscreen_window.attributes('-fullscreen', True)
        self.fullscreen_window.bind('<Escape>', self.exit_fullscreen)
        self.fullscreen_window.bind('<Button-1>', self.on_click)

        self.canvas = Canvas(self.fullscreen_window, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Convert screenshot to Tkinter image format
        self.image = ImageTk.PhotoImage(self.screenshot)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

        self.start_x = self.start_y = 0
        self.rect = None

    def on_click(self, event):
        if not self.rect:
            self.start_x = event.x
            self.start_y = event.y
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline='green', width=2)
            self.canvas.bind('<B1-Motion>', self.draw_rectangle)
            self.canvas.bind('<ButtonRelease-1>', self.select_region)
        else:
            self.select_region(event)

    def draw_rectangle(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def select_region(self, event):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        self.selected_region = (int(x1), int(y1), int(x2), int(y2))
        self.fullscreen_window.destroy()  # Close the fullscreen window
        self.root.deiconify()  # Show the main window again

        # Show preview window
        self.show_preview()

    def show_preview(self):
        self.preview_window = tk.Toplevel(self.root)
        self.preview_window.title("Preview")

        # Center the preview window
        self.center_window(self.preview_window)

        # Check if a region is selected; if not, use the full screenshot
        if not hasattr(self, 'selected_region') or self.selected_region is None:
            self.selected_region = (0, 0, self.screenshot.width, self.screenshot.height)

        # Crop the selected region from the screenshot
        x1, y1, x2, y2 = self.selected_region
        region_image = self.screenshot.crop((x1, y1, x2, y2))

        # Get the size of the preview window
        self.preview_window.update_idletasks()  # Ensure window size is updated
        window_width = self.preview_window.winfo_width()
        window_height = self.preview_window.winfo_height()

        # Resize image if it's too large for the window
        image_width, image_height = region_image.size
        if image_width > window_width or image_height > window_height:
            max_width = window_width - 20  # Leave some padding
            max_height = window_height - 40  # Leave some padding

            # Calculate new size maintaining the aspect ratio
            ratio = min(max_width / image_width, max_height / image_height)
            new_size = (int(image_width * ratio), int(image_height * ratio))

            # Ensure new_size has valid dimensions
            new_size = (max(1, new_size[0]), max(1, new_size[1]))

            resized_image = region_image.resize(new_size, Image.LANCZOS)
        else:
            resized_image = region_image

        self.preview_image = ImageTk.PhotoImage(resized_image)

        preview_canvas = Canvas(self.preview_window, width=resized_image.width, height=resized_image.height)
        preview_canvas.pack(fill=tk.BOTH, expand=True)
        preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_image)

        save_button = Button(self.preview_window, text="Save", command=self.save_image)
        save_button.pack(side=tk.RIGHT, padx=10, pady=10)

        cancel_button = Button(self.preview_window, text="Cancel", command=self.cancel_preview)
        cancel_button.pack(side=tk.LEFT, padx=10, pady=10)
    def save_image(self):
        # Ensure save directory is valid
        if not os.path.isdir(self.save_directory):
            # Save to the current working directory if invalid
            self.save_directory = os.getcwd()
            self.save_settings()

        # Determine the file path with incremental number to avoid overwriting
        base_name = "screenshot"
        file_extension = ".png"
        file_path = os.path.join(self.save_directory, base_name + file_extension)
        counter = 1

        while os.path.isfile(file_path):
            file_path = os.path.join(self.save_directory, f"{base_name}_{counter}{file_extension}")
            counter += 1

        try:
            self.screenshot.crop(self.selected_region).save(file_path)
        except SystemError:
            self.preview_window.destroy()
            messagebox.showerror("Invalid Screenshot", "Not saved. Insufficient box size")
        else:
            self.preview_window.destroy()
            self.root.quit()  # Close the main loop

    def cancel_preview(self):
        self.preview_window.destroy()  # Only destroy the preview window

    def exit_fullscreen(self, event):
        self.fullscreen_window.destroy()
        self.root.deiconify()  # Show the main window again

    def save_settings(self):
        settings = {
            'save_directory': self.save_directory,
            'delay': self.delay
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.save_directory = settings.get('save_directory', os.getcwd())
                self.delay = settings.get('delay', 0)
        else:
            self.save_directory = os.getcwd()
            self.delay = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()
