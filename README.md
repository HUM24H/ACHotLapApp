# Assetto Corsa Hotlap Generator App
## Disclaimer
This was a personal project, it is not something I would recommend people actively use even if you find this something useful. I did this as a challenge to work on my skills in Python and with building GUI apps, this app does mostly work but it is rough and has some bugs.

If you want to fork/clone this repo and completely re-write or update this app to fit your needs or to get working for a Production environment, then please feel free to do so.

## How it works
### Initial Opening
To use the app, you need to run the .exe binary inside the "dist" folder called: FrontEnd.exe

On first opening, you will be asked to location and select your Assetto Corsa root install directory.

<img width="2064" height="987" alt="image" src="https://github.com/user-attachments/assets/134d01ee-552a-4b1a-874e-9b5c132108b8" />

If you provide an invalid path, you will be given an error and the option to select a new path.

<img width="596" height="673" alt="image" src="https://github.com/user-attachments/assets/147c90de-57a6-44c5-9e9e-9deb22b49861" />

Once you have selected a new path, a message will pop-up to confirm this and then you can use the App.

<img width="586" height="662" alt="image" src="https://github.com/user-attachments/assets/cbfb9389-8f85-4b52-abfd-d09de5e97f0e" />

### Main App Form
The main form will contain a few fields that you can interact with.

The first two being drop down's which are populated using your Assetto Corsa Content that you have installed, these will contain a list of Cars & Tracks.

The Car list is simply taking the Car Name from the ui_car.json file in the car install location, this allows for an easily readable name for you to select but under the head we have a mapping list so that once you select a car we can map what you selected to that cars physical folder name which is used in the Special Event .ini file.

<img width="569" height="658" alt="image" src="https://github.com/user-attachments/assets/978494e6-c85b-4a36-a622-fdaca4f667f9" />

The Track list is a bit more weird! The way I have layed it out is that you have each track and its variant with the parent folder name of that track at the start of each entry, the reason for this is because some tracks name in ui_track.json is simple "2022" or "GP" which is not understandable so I added the parent folder name to add more context to the name.

Like with the Car list, under the head there is a mapping list so that when you select a track we can get the Parent & Variant folder names which is used in the Special Event .inii file.

<img width="574" height="648" alt="image" src="https://github.com/user-attachments/assets/093965bd-94e2-4b05-af5c-c52d29176afe" />

### Setting Times
The last part of the form is the "Base Time" and the 3 time boxes underneath it.

This is where you will set the reference time to which the Gold, Silver & Bronze times will be calcualted from. The values for each of these is: 2.5%, 5.0% 7 10.0% and these are done against the "Base Time" you set.

The "Base Time" does need to be in a format of: mm:ss.ms (01:22.231) - the form will not calculate the other times and will show a red error text at the bottom if the "Base Time" is not in the expected format.

<img width="570" height="649" alt="image" src="https://github.com/user-attachments/assets/d9fb501e-330b-47db-8096-22c90ec3cb8d" />

Once you have filled in the form then all that is left is to hit the "Generate" button and immediately if you go into Content Manager --> Challenges --> HOTLAPS, you will now see your new Hotlap event.

<img width="2834" height="506" alt="image" src="https://github.com/user-attachments/assets/51fdc1f8-e400-4ecc-9552-671c4f887275" />

There can be some minor discrepancies with the times, only out by a few milliseconds and this is just down to how the app is calculating the time and how Assetto Corsa stores time in the .ini file for the Special Event.

## Final Note
As said at the top, this was a personal project to challenge myself with a Python app that uses a GUI. While this app does somewhat work for the most part, there are still some bugs and issues as I cannot cater for every single installation scenario of Assetto Corsa content - so this app works well enough on my installation of Assetto Corsa.
