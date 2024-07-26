# Simple_Screenshot

This is a Python application that allows users to take screenshots with a configurable delay and preview them before saving. The app uses `tkinter` for the graphical user interface and `pyautogui` for capturing screenshots. Users can select a region to capture, apply a delay, and choose a save directory.

## Features

- **Select Directory**: Choose where to save screenshots.
- **Configurable Delay**: Set a delay before the screenshot is captured.
- **Full Screenshot**: Capture a full-screen screenshot.
- **Preview and Save**: Preview the screenshot and save it to the selected directory.
- **Region Selection**: Draw a rectangle to select a specific region for capturing.

## Installation

Ensure you have Python installed. Then, install the required packages using pip:
```bash
pip install -r requirements.txt
```
## Usage
1. Launch the Application: Run the script using Python.
```bash
python screenshot_app.py
```
2. Select Directory: Click on the "Select Directory to Save" button to choose where the screenshots will be saved. The path is automatically saved for future use.
3. Set Delay: Enter the delay in seconds in the provided text box. This delay will be applied before the screenshot is captured.
4. Start Capturing:
   Click "Start Capturing" to take a full-screen screenshot after the specified delay.
   Alternatively, click "Take Full Screenshot" to capture a full-screen image directly.
6. Preview and Save:
  After capturing, the preview window will open. You can select a region to crop if needed.
  Click "Save" to save the screenshot to the selected directory or "Cancel" to discard it.
7. Fullscreen Mode:
   In the preview window, you can view the screenshot in fullscreen mode.
   Press Escape to exit fullscreen mode.
## Configuration
* Settings such as the save directory and delay are stored in settings.json and will be loaded on the next start.
## Note:
* Invalid Input Error: Ensure that the delay is an integer and not negative.
* Save Directory: If the save directory is invalid, the app will use the current working directory.
## License
This project is licensed under the Unlicense - see the [LICENSE](LICENSE) file for details.

