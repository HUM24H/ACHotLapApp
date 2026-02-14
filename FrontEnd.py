import os
import re
import threading
import FileOperations 
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

# Variables for percentage time calculation
aTimePercVals = [2.5, 5.0, 10.0]
aResultVars = []

# Variables used to dynamically build time fields on form
iXAxisLabel = 50
iXAxisEntry = 150
iYAxisStart = 160
iRowHeight = 40

# Lists & Mappings for Car & Track data
aCarVals = []
aTrackVals = []
aCarFolders = {}
aTrackFolders = {}

# Store selected values for use when generating Special Events .ini file
sSelectedCar=""
sSelectedCarFolder=""
sSelectedTrackName=""
sSelectedTrackFolder=""
sSelectedParentTrackFolder=""
aSelectedTimes=[]

# Variable to store the AC root install location
sRootInstall = ""

# Classes for Loading Form & AC Root Install Form
class LoadingDialog(tk.Toplevel):
    def __init__(self, parent, text="Loading data…"):
        super().__init__(parent)

        # Set title of Loading Form
        self.title("Please wait")
        self.transient(parent)

        # Add label for given Text value
        ttk.Label(self, text=text, padding=20).pack()

        self.update_idletasks()

        # Align Loading Form with center point of Main Form
        iXAxis = parent.winfo_rootx() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        iYAxis = parent.winfo_rooty() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{iXAxis}+{iYAxis}")

        self.grab_set()

    def close(self):
        # Close and destroy Loading form once complete
        self.grab_release()
        self.destroy()

class AssettoCorsaPathPicker:
    def __init__(self):
        # Create a hidden root window to house the dialogs
        self.root = tk.Tk()
        self.root.withdraw()
        self.executable_name = "AssettoCorsa.exe"

    def get_path(self):
        # Allow user to select AC root install directory
        while True:
            selected_path = filedialog.askdirectory(
                title="Select Assetto Corsa Root Installation Directory"
            )

            # Allow user to select again if they cancel
            if not selected_path:
                if messagebox.askretrycancel("No Path Selected", "You didn't select a folder. Would you like to try again?"):
                    continue
                else:
                    return None

            # Check for the executable
            exe_path = os.path.join(selected_path, self.executable_name)
            
            if os.path.isfile(exe_path):
                # Successfully found correct AC root install folder
                messagebox.showinfo("Success", "Assetto Corsa installation verified!")
                self.root.destroy()
                return os.path.normpath(selected_path)
            else:
                # Allow user to select again if incorrect path selected
                try_again = messagebox.askretrycancel(
                    "Invalid Directory", 
                    f"Could not find '{self.executable_name}' in:\n{selected_path}\n\nPlease select the root folder."
                )
                if not try_again:
                    self.root.destroy()
                    return None

# Functions for Parsing & Formatting inputted time
def parse_time(text: str):
    # Check time value matches expected format
    m = re.fullmatch(r"\s*(\d+):([0-5]?\d(?:\.\d{1,3})?)\s*", text)

    # Return none if incorrect format
    if not m:
        return None
    
    # Format into seconds for return value
    minutes = int(m.group(1))
    seconds = float(m.group(2))
    return minutes * 60 + seconds

def format_time(seconds: float) -> str:
    # Format seconds into display format
    minutes = int(seconds // 60)
    secs = seconds % 60

    ms_str = f"{secs:.3f}".rstrip('0').rstrip('.')

    return f"{minutes:02d}:{ms_str.zfill(2)}"

# Cars & Tracks ComboBox Handlers
def sel_change_car(event):
    global sSelectedCar
    global sSelectedCarFolder

    # Get selected car from combo box
    widget = event.widget
    sSelectedCar = widget.get()

    # Fetch correct folder for selected car
    sSelectedCarFolder = aCarFolders.get(sSelectedCar, "<unknown>")

def sel_change_track(event):
    global sSelectedTrackName
    global sSelectedTrackFolder
    global sSelectedParentTrackFolder

    # Get selected track from combo box
    widget = event.widget
    selected_track = widget.get()

    # Fetch correct folder & parent folder for selected track
    if selected_track in aTrackFolders:
        data = aTrackFolders[selected_track]

        sSelectedTrackName = selected_track
        sSelectedTrackFolder = data['folder']
        sSelectedParentTrackFolder = data['parent']

# Function to exit program
def exit_program(event=None):
    window.destroy()

# Wrapper Function for creating Special Event .ini file
def generate_event(event=None):
    create_new_special_event(sSelectedTrackName, sSelectedParentTrackFolder, sSelectedTrackFolder, sSelectedCarFolder, aSelectedTimes)

    messagebox.showinfo("Success", "Assetto Corsa Special Event Generated!")

# Function to create Special Event .ini file
# Uses pre-defined template as we only need to change a few data points
def create_new_special_event(track_name, parent_folder, track_folder, car_folder, times):
    # Create base path for Special Event file
    base_path = os.path.join(sRootInstall, "content/specialevents")
    
    # Find the next Special Event ID
    # This takes the current latest number and we then increment that
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

    # Assign and create new Special Event folder with new ID
    next_id = max(ids) + 1 if ids else 1
    new_folder_name = f"SPECIAL_EVENT_{next_id}"
    new_folder_path = os.path.join(base_path, new_folder_name)

    # Create the new directory
    os.makedirs(new_folder_path, exist_ok=True)

    # Prepare the condition times
    obj_2 = int(times[0] * 1000)
    obj_1 = int(times[1] * 1000)
    obj_0 = int(times[2] * 1000)

    # Uses pre-defined format with some elements changing
    # Doing this as we only need to change a few elements
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
    global aCarVals
    global aTrackVals

    try:
        # Fetch Car & Track list from AC root install
        aCarVals = FileOperations.processCarList(sRootInstall)
        aTrackVals = FileOperations.processTrackList(sRootInstall)

        # Create folder mappings to be used later
        create_car_folder_mapping()
        create_track_folder_mapping()
    except Exception as exc:
        window.after(0, lambda: messagebox.showerror("Error", str(exc)))
        return

    window.after(0, lambda: populate_comboboxes())

def populate_comboboxes():
    # Populate car combo box using folder mapping key values
    car_names = sorted(aCarFolders.keys()) 
    combo_car["values"] = car_names

    # Populate track combo box using folder mapping key values
    track_names = sorted(aTrackFolders.keys())
    combo_track["values"] = track_names

    # Set combo boxes to enabled
    combo_car.state(["!disabled"])
    combo_track.state(["!disabled"])

    loading_dialog.close()

def create_car_folder_mapping():
    global aCarFolders
    
    # Loop through car values and assign their folder name to new list
    # Uses car human-readable name as key value
    for i in range(0, len(aCarVals), 2):
        car = aCarVals[i]
        folder = aCarVals[i + 1]
        aCarFolders[car] = folder

def create_track_folder_mapping():
    global aTrackFolders
    
    skip_next = False

    # Loop through track values and assign their folder name to new list
    for i in range(len(aTrackVals)):
        current_item = aTrackVals[i]

        # Skip current element if set
        if skip_next:
            skip_next = False
            continue
        
        # Store track parent folder name for use later
        if '#' in current_item:
            current_parent = current_item.lstrip("#")
            continue
        
        # Grab current track variant folder name
        if i + 1 < len(aTrackVals):
            folder_name = aTrackVals[i + 1]
        
        # Set display name for combo box and key value
        display_name = f"{current_parent} | {current_item}"
        
        # Assign parent folder and variant folder to mapping list
        # Uses display name as the key value
        aTrackFolders[display_name] = {
            "folder": folder_name,
            "parent": current_parent
        }

        # Set to skip next element as we want to process every other element
        skip_next = True

# Function to calculate percetage times based on given time from user
def recalc_aTimePercVals(*_):
    # Get inputted base time value
    # Check time matches expected format
    txt = base_time_var.get()
    secs = parse_time(txt)

    # Reset current time percentage fields
    # Return error higlighting format match issue
    if secs is None:
        for v in aResultVars:
            v.set("")

        status_lbl.config(text="Enter time as mm.ss.ms (e.g. 01:23.456)")

        return

    # Empty label text if no error
    status_lbl.config(text="")

    # Clear selected time list
    aSelectedTimes.clear()

    # Generate new percentage times based off of base time
    # Assign new second values to the selected times list
    for pct, var in zip(aTimePercVals, aResultVars):
        new_secs = secs + (secs * (pct / 100.0))
        var.set(format_time(new_secs))
        aSelectedTimes.append(new_secs)

# UI Constructions
window = tk.Tk()
window.title("AC Hotlap Generator")
window.geometry("375x400")
window.eval('tk::PlaceWindow . center')
window.resizable(False, False)

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

exit_btn = tk.Button(window, text="Exit")
exit_btn.place(x=25, y=325)
exit_btn.bind("<Button-1>", exit_program)

gen_btn = tk.Button(window, text="Generate")
gen_btn.place(x=100, y=325)
gen_btn.bind("<Button-1>", generate_event)

# Status text for error when processing base time
status_lbl = ttk.Label(window, text="", foreground="red")
status_lbl.place(x=100, y=375)

# Dynamically build the time fields
# Needed as we have 4 fields with 3 being read-only and needing to be placed in specific location
# Base time label
ttk.Label(window, text="Base time").place(x=iXAxisLabel, y=iYAxisStart)

# Base time field
base_time_var = tk.StringVar()
base_entry = ttk.Entry(window, textvariable=base_time_var, width=12)
base_entry.place(x=iXAxisEntry, y=iYAxisStart)
base_entry.bind("<KeyRelease>", recalc_aTimePercVals)

# Percentage fields
for idx, pct in enumerate(aTimePercVals, start=1):
    row_y = iYAxisStart + idx * iRowHeight

    # Percentage label
    ttk.Label(window, text=f"{pct:g}%").place(x=iXAxisLabel, y=row_y)

    # Percentage field to hold calculated time
    # This is done off of the inputted base time
    var = tk.StringVar()
    aResultVars.append(var)
    out_entry = ttk.Entry(window, textvariable=var, width=12, state="readonly")
    out_entry.place(x=iXAxisEntry, y=row_y)

# Function for the loading of data in a thread
def show_loading_and_start_worker():
    global loading_dialog
    global sRootInstall

    # Ask for AC root install path
    picker = AssettoCorsaPathPicker()
    ac_path = picker.get_path()

    # Validate we have the correct path
    # If not we destroy and exit
    if ac_path:
        sRootInstall = ac_path
    else:
        window.destroy()
        return False

    # Setup thread to show Loading Form and assign data to combo boxes
    loading_dialog = LoadingDialog(window, text="Loading car & track data…")
    threading.Thread(target=load_combobox_data, daemon=True).start()

# Assign task for form after initial start
window.after_idle(show_loading_and_start_worker)

# Start App
window.mainloop()