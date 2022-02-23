import datetime
from time import sleep
import subprocess
# import webbrowser
import pyautogui as pg
from pytesseract import pytesseract, image_to_string

"""
How to use:
1. Install whatever imports you need. (Probably pyautogui, opencv-python, pytesseract)
2. CTRL+F subprocess.Popen(...) and replace the inside with the path for your zoom.exe file on your computer
3. CTRL+F my_thing. Create meeting object. 
   Ex: my_thing = meeting(start_time, end_time, meeting_id)  
"""

"""
Mon/Wed
Math 270B: 835 5497 1111 (14:30 - 15:30)
CS 240: 997 5604 8746 (20:00 - 21:50)

Tues/Thurs
Music 100: 836 6445 1242 (20:30 - 21:30)
CS 233: 814 0991 5762 (19:30 - 21:20)
"""


class meeting:
    def __init__(self, start_time: str, end_time: str, meeting_id: str = "", url: str = ""):
        self.meeting_id = meeting_id
        self.url = url
        self.start_time = datetime.datetime.strptime(start_time, "%H:%M")
        self.end_time = datetime.datetime.strptime(end_time, "%H:%M")


def enter_zoom(meeting_id: str):
    # Step 0: Press esc to exit out of sidebar, windows key overlay, task manager, etc.
    pg.hotkey("esc")
    pg.hotkey("esc")
    pg.hotkey("esc")

    # Step 1: Open zoom
    pg.hotkey("win", "d")
    subprocess.Popen(r"C:\Users\yugin\AppData\Roaming\Zoom\bin\Zoom.exe")

    sleep(3)

    # Step 2: Click join button
    join = pg.locateCenterOnScreen("join.jpg", confidence=0.95)  # Use r"" with direct path if necessary
    pg.click(join)

    sleep(1)

    # Step 3: Enter meeting id and join
    meetingid = pg.locateCenterOnScreen("meetingid.jpg", confidence=0.8)
    pg.click(meetingid)
    pg.typewrite(meeting_id)

    meetingjoin = pg.locateCenterOnScreen("meetingjoin.jpg", confidence=0.8)
    pg.click(meetingjoin)

    sleep(3)

    # Step 4: Find number of participants
    participants = pg.locateOnScreen("participants.jpg", confidence=0.9)
    if not participants:
        pg.hotkey("alt", "u")
        participants = pg.locateOnScreen("participants.jpg", confidence=0.9)

    # participants = Box(left=1693, top=46, width=78, height=16), increases left by width. Then sets width to 30 pixels to the right of it
    pg.screenshot(region=(participants[0] + participants[2], participants[1], 30, participants[3])).save(
        "participants_number.jpg")


def leave_zoom(host: bool = False):
    pg.hotkey("esc")
    pg.hotkey("esc")
    pg.hotkey("esc")

    pg.hotkey("alt", "q")
    if host:
        hostleave = pg.locateCenterOnScreen("hostleave.jpg", confidence=0.9)
        pg.click(hostleave)


# Necessary to use pytesseract
pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
host_id = "849 020 1718"
current_time = datetime.datetime.now()

# TIMES HAVE TO BE FROM 0-23, NOT 0-12
my_thing = meeting("19:31", "19:30", "814 0991 5762")

# For joining zoom
while True:
    current_time = datetime.datetime.now()

    if current_time.hour == my_thing.start_time.hour:
        if current_time.minute == my_thing.start_time.minute:
            enter_zoom(my_thing.meeting_id)
            break

    sleep(60)

# For leaving zoom (runs after the first while loop breaks = entered zoom)
max_participants = 0
while True:
    current_time = datetime.datetime.now()

    # Leave zoom if end_time
    if current_time.hour == my_thing.end_time.hour:
        if current_time.minute == my_thing.end_time.minute:
            # Different way to leave if you are hosting meeting
            if my_thing.meeting_id == host_id:
                leave_zoom(host=True)
            else:
                leave_zoom()
            break

    # Leave zoom if participant number <50% of max participants
    num_participants = int("".join([i for i in image_to_string("participants_number.jpg") if i.isdigit()]))

    print(f"{max_participants = }")

    # Update number of participants
    participants = pg.locateOnScreen("participants.jpg", confidence=0.9)
    if not participants:
        pg.hotkey("alt", "u")
        participants = pg.locateOnScreen("participants.jpg", confidence=0.9)
    try:
        pg.screenshot(region=(participants[0] + participants[2], participants[1], 30, participants[3])).save(
            "participants_number.jpg")
    except TypeError:
        pass

    if max_participants < num_participants:
        max_participants = num_participants

    if num_participants <= (max_participants * .80):
        if my_thing.meeting_id == host_id:
            leave_zoom(host=True)
        else:
            leave_zoom()
        break

    sleep(30)
