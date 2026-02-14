import os
import re
import threading
import ProcessingData 
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

PERCENTAGES = [2.5, 5.0, 10.0]
result_vars = []

car_vals = []
track_vals = []
car_folders = {}
track_folders = {}

selected_car=""
selected_car_folder=""
selected_track_name=""
selected_track_folder=""
selected_track_parent_folder=""
selected_times=[]

root_install = ""

# Classes for Loading Form & AC Root Install Form
class LoadingDialog(tk.Toplevel):
    def __init__(self, parent, text="Loading data…"):
        super().__init__(parent)
        self.title("Please wait")
        self.transient(parent)
        ttk.Label(self, text=text, padding=20).pack()
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        self.grab_set()

    def close(self):
        self.grab_release()
        self.destroy()

class AssettoCorsaPathPicker:
    def __init__(self):
        # Create a hidden root window to house the dialogs
        self.root = tk.Tk()
        self.root.withdraw()
        self.executable_name = "AssettoCorsa.exe"

    def get_path(self):
        while True:
            selected_path = filedialog.askdirectory(
                title="Select Assetto Corsa Root Installation Directory"
            )

            # If user cancels the directory picker
            if not selected_path:
                if messagebox.askretrycancel("No Path Selected", "You didn't select a folder. Would you like to try again?"):
                    continue
                else:
                    return None

            # Validation: Check for the executable
            exe_path = os.path.join(selected_path, self.executable_name)
            
            if os.path.isfile(exe_path):
                messagebox.showinfo("Success", "Assetto Corsa installation verified!")
                self.root.destroy()
                return os.path.normpath(selected_path)
            else:
                # Error: File not found in selected directory
                try_again = messagebox.askretrycancel(
                    "Invalid Directory", 
                    f"Could not find '{self.executable_name}' in:\n{selected_path}\n\nPlease select the root folder."
                )
                if not try_again:
                    self.root.destroy()
                    return None

# Functions for Parsing & Formatting inputted time
def parse_time(text: str):
    m = re.fullmatch(r"\s*(\d+):([0-5]?\d(?:\.\d{1,3})?)\s*", text)
    if not m:
        return None
    minutes = int(m.group(1))
    seconds = float(m.group(2))
    return minutes * 60 + seconds

def format_time(seconds: float) -> str:
    minutes = int(seconds // 60)
    secs = seconds % 60
    ms_str = f"{secs:.3f}".rstrip('0').rstrip('.')
    return f"{minutes:02d}:{ms_str.zfill(2)}"

# Cars & Tracks ComboBox Handlers
def sel_change_car(event):
    global selected_car
    global selected_car_folder

    widget = event.widget
    selected_car = widget.get()
    selected_car_folder = car_folders.get(selected_car, "<unknown>")

def sel_change_track(event):
    global selected_track_name
    global selected_track_folder
    global selected_track_parent_folder

    widget = event.widget
    selected_track = widget.get()

    if selected_track in track_folders:
        data = track_folders[selected_track]

        selected_track_name = selected_track
        selected_track_folder = data['folder']
        selected_track_parent_folder = data['parent']

# Function to exit program
def exit_program(event=None):
    window.destroy()

# Wrapper Function for creating Special Event .ini file
def generate_event(event=None):
    create_new_special_event(selected_track_name, selected_track_parent_folder, selected_track_folder, selected_car_folder, selected_times)

# Function to create Special Event .ini file
# Uses pre-defined template as we only need to change a few data points
def create_new_special_event(track_name, parent_folder, track_folder, car_folder, times):
    base_path = os.path.join(root_install, "content/specialevents")
    
    # Find the next ID
    existing_folders = [f for f in os.listdir(base_path) if f.startswith("SPECIAL_EVENT_")]
    
    ids = []

    for folder in existing_folders:
        try:
            # Extract the number at the end using regex or splitting
            match = re.search(r'SPECIAL_EVENT_(\d+)', folder)
            if match:
                ids.append(int(match.group(1)))
        except ValueError:
            continue

    next_id = max(ids) + 1 if ids else 1
    new_folder_name = f"SPECIAL_EVENT_{next_id}"
    new_folder_path = os.path.join(base_path, new_folder_name)

    # Create the new directory
    os.makedirs(new_folder_path, exist_ok=True)

    # Prepare the content (Mapping Condition 0, 1, 2 to indices 2, 1, 0)
    # Using 1000 multiplier to match your example (106s -> 106000)
    obj_2 = int(times[0] * 1000)
    obj_1 = int(times[1] * 1000)
    obj_0 = int(times[2] * 1000)

    content = f"""[EVENT]
NAME={track_name} Sprint
DESCRIPTION=Hotlap

[SPECIAL_EVENT]
GUID={363 + next_id}  # Example: incrementing GUID as well

[RACE]
TRACK={parent_folder}
CONFIG_TRACK={track_folder}
MODEL={car_folder}
CARS=1
PENALTIES=1
FIXED_SETUP=0
MODEL_CONFIG=
AI_CLASS=street

[CAR_0]
MODEL=-
SKIN=
DRIVER_NAME=Ramon Castillo
NATIONALITY=Planet Earth
SETUP=
MODEL_CONFIG=

[GHOST_CAR]
RECORDING=0
PLAYING=0
SECONDS_ADVANTAGE=0
LOAD=1
FILE=
ENABLED=0

[LIGHTING]
SUN_ANGLE=16
TIME_MULT=1
CLOUD_SPEED=0.2

[GROOVE]
VIRTUAL_LAPS=10
MAX_LAPS=1
STARTING_LAPS=1

[TEMPERATURE]
AMBIENT=22
ROAD=27

[WEATHER]
NAME=3_clear

[SESSION_0]
NAME=Hotlap
TYPE=4
SPAWN_SET=HOTLAP_START

[CONDITION_0]
TYPE=TIME
OBJECTIVE={obj_0}

[CONDITION_1]
TYPE=TIME
OBJECTIVE={obj_1}

[CONDITION_2]
TYPE=TIME
OBJECTIVE={obj_2}

[DYNAMIC_TRACK]
PRESET=5
LAP_GAIN=1
RANDOMNESS=0
SESSION_START=100
SESSION_TRANSFER=100

[LAP_INVALIDATOR]
ALLOWED_TYRES_OUT=0"""

    # Write the file
    file_path = os.path.join(new_folder_path, "event.ini")
    with open(file_path, "w") as f:
        f.write(content)

    return f"Created {new_folder_name}/event.ini successfully."

# Thread code used when form initially starts
# Used in conjuction with Loading Form class
def load_combobox_data():
    global car_vals
    global track_vals

    try:
        car_vals = ProcessingData.processCarList(root_install)
        track_vals = ProcessingData.processTrackList(root_install)

        create_car_folder_mapping()
        create_track_folder_mapping()
    except Exception as exc:
        window.after(0, lambda: messagebox.showerror("Error", str(exc)))
        return

    window.after(0, lambda: populate_comboboxes())

def populate_comboboxes():
    car_names = sorted(car_folders.keys()) 
    combo_car["values"] = car_names

    track_names = sorted(track_folders.keys())
    combo_track["values"] = track_names

    combo_car.state(["!disabled"])
    combo_track.state(["!disabled"])

    loading_dialog.close()

def create_car_folder_mapping():
    global car_folders
    
    for i in range(0, len(car_vals), 2):
        car = car_vals[i]
        folder = car_vals[i + 1]
        car_folders[car] = folder

def create_track_folder_mapping():
    global track_folders
    
    skip_next = False

    for i in range(len(track_vals)):
        current_item = track_vals[i]

        if skip_next:
            skip_next = False
            continue

        if '#' in current_item:
            current_parent = current_item.lstrip("#")
            continue
        
        if i + 1 < len(track_vals):
            folder_name = track_vals[i + 1]
        
        display_name = f"{current_parent} | {current_item}"
        
        track_folders[display_name] = {
            "folder": folder_name,
            "parent": current_parent
        }

        skip_next = True

# Function to calculate percetage times based on given time from user
def recalc_percentages(*_):
    txt = base_time_var.get()
    secs = parse_time(txt)

    if secs is None:
        for v in result_vars:
            v.set("")
        status_lbl.config(text="Enter time as mm.ss.ms (e.g. 01:23.456)")
        return

    status_lbl.config(text="")

    selected_times.clear()

    for pct, var in zip(PERCENTAGES, result_vars):
        new_secs = secs + (secs * (pct / 100.0))
        var.set(format_time(new_secs))
        selected_times.append(new_secs)

# UI Constructions
window = tk.Tk()
window.title("AC Hotlap Generator")
window.geometry("375x400")
window.eval('tk::PlaceWindow . center')
window.resizable(False, False)

exit_btn = tk.Button(window, text="Exit")
exit_btn.place(x=25, y=350)
exit_btn.bind("<Button-1>", exit_program)

gen_btn = tk.Button(window, text="Generate")
gen_btn.place(x=100, y=350)
gen_btn.bind("<Button-1>", generate_event)

combo_car = ttk.Combobox(window, state="disabled", width=30)
combo_car.place(x=75, y=50)
combo_car.bind("<<ComboboxSelected>>", sel_change_car)
lbl_car = ttk.Label(window, text="Cars")
lbl_car.place(x=25, y=50)

combo_track = ttk.Combobox(window, state="disabled", width=30)
combo_track.place(x=75, y=100)
combo_track.bind("<<ComboboxSelected>>", sel_change_track)
lbl_track = ttk.Label(window, text="Tracks")
lbl_track.place(x=25, y=100)

# Dynamically build the time fields
# Needed as we have 4 fields with 3 being read-only and needing to be placed in specific locations
BASE_X_LABEL = 50          # left edge for the percentage labels
BASE_X_ENTRY = 150         # left edge for the entry fields
START_Y = 160              # first row (base‑time entry) starts here
ROW_H = 40                 # vertical distance between rows

# Base‑time entry (editable)
ttk.Label(window, text="Base time").place(x=BASE_X_LABEL, y=START_Y)
base_time_var = tk.StringVar()
base_entry = ttk.Entry(window, textvariable=base_time_var, width=12)
base_entry.place(x=BASE_X_ENTRY, y=START_Y)
base_entry.bind("<KeyRelease>", recalc_percentages)

# Result rows (read‑only) + percentage labels
for idx, pct in enumerate(PERCENTAGES, start=1):
    row_y = START_Y + idx * ROW_H

    # Percentage label (small box)
    ttk.Label(window, text=f"{pct:g}%").place(x=BASE_X_LABEL, y=row_y)

    # Read‑only entry that will hold the calculated time
    var = tk.StringVar()
    result_vars.append(var)
    out_entry = ttk.Entry(window, textvariable=var, width=12, state="readonly")
    out_entry.place(x=BASE_X_ENTRY, y=row_y)

# Status line for validation messages (below the calculator)
status_lbl = ttk.Label(window, text="", foreground="red")
status_lbl.place(x=BASE_X_LABEL, y=START_Y + (len(PERCENTAGES) + 2) * ROW_H)

# Function for the loading of data in a thread
def show_loading_and_start_worker():
    global loading_dialog
    global root_install

    picker = AssettoCorsaPathPicker()
    ac_path = picker.get_path()

    if ac_path:
        root_install = ac_path
    else:
        window.destroy()
        return False

    loading_dialog = LoadingDialog(window, text="Loading car & track data…")
    threading.Thread(target=load_combobox_data, daemon=True).start()

window.after_idle(show_loading_and_start_worker)

# Start App
window.mainloop()