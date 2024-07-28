# OLD PROJECT
# Zoom Automator

Zoom Automator is a Python script designed to automate the process of joining and leaving Zoom meetings. It uses `pytesseract` for OCR to read the number of participants in a meeting.

## Features

- Automatically joins Zoom meetings at specified times.
- Automatically leaves Zoom meetings at specified end times or when the number of participants drops below a threshold.
- Uses OCR to read the number of participants in a meeting.

## Requirements

- Python 3.x
- `pyautogui`
- `opencv-python`
- `pytesseract`

## Setup

1. Install the required Python packages:
    ```sh
    pip install pyautogui opencv-python pytesseract
    ```

2. Create a .env file and set the `ZOOM_FILE` variable in the script with the path to your `Zoom.exe` file. Do the same with your zoom host id and pytesseract, "HOST_ID" and "PYTESSERACT", respectively.

3. Ensure `pytesseract` is correctly installed and configured on your system.

## Usage

1. Define your meetings in the `all_meetings` list:
    ```python
    current_time = datetime.datetime.now()
    all_meetings = [
        Meeting(current_time, current_time + datetime.timedelta(minutes=1), "MEETING_ID", "PASSWORD")
    ]
    ```

2. Run the script:
    ```sh
    python "path/to/Zoom Automator.py"
    ```

## Code Overview

### Main Functions

- `click_on_image(image: str, confidence: float = 0.8)`: Clicks on an image on the screen.
- `enter_zoom(meeting: Meeting)`: Enters a Zoom call.
- `leave_zoom(meeting_id: str = "")`: Leaves a Zoom call.
- `check_start_times(meetings_list: list) -> Meeting | None`: Returns a `Meeting` object if there is a meeting about to start.
- `check_end_times(meetings_list: list) -> Meeting | None`: Returns a `Meeting` object if there is a meeting about to end.

### Main Loop

The `main` function contains two loops:
1. The first loop checks for meeting start times and joins the meeting when it's time.
2. The second loop checks for meeting end times or participant count and leaves the meeting accordingly.
