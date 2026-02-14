# Assetto Corsa Hotlap Generator App
## Disclaimer
This was a personal project, it is not something I would recommend people actively use even if you find this something useful. I did this as a challenge to work on my skills in Python and with building GUI apps, this app does mostly work but it is rough and has some bugs.

If you want to fork/clone this repo and completely re-write or update this app to fit your needs or to get working for a Production environment, then please feel free to do so.

## How it works
### Initial Opening
To use the app, you need to run the .exe binary inside the "dist" folder called: ACHotLapApp.exe

On first opening, you will be asked to location and select your Assetto Corsa root install directory.

<img width="2090" height="970" alt="image" src="https://github.com/user-attachments/assets/0fa982ae-3690-421c-96a5-1bd50a6a65d5" />

If you provide an invalid path, you will be given an error and the option to select a new path.

<img width="573" height="648" alt="image" src="https://github.com/user-attachments/assets/64423bd3-7f06-4ef0-ad43-74611fd129e5" />

Once you have selected a new path, a message will pop-up to confirm this and then you can use the App.

<img width="578" height="661" alt="image" src="https://github.com/user-attachments/assets/fb021b8e-1431-4b39-9671-4df0337d814e" />

### Main App Form
The main form will contain a few fields that you can interact with.

The first two being drop down's which are populated using your Assetto Corsa Content that you have installed, these will contain a list of Cars & Tracks.

The Car list is simply taking the Car Name from the ui_car.json file in the car install location, this allows for an easily readable name for you to select but under the head we have a mapping list so that once you select a car we can map what you selected to that cars physical folder name which is used in the Special Event .ini file.

<img width="566" height="654" alt="image" src="https://github.com/user-attachments/assets/cb1317ed-ab6e-450e-91a3-174c6ddf373e" />

The Track list is a bit more weird! The way I have layed it out is that you have each track and its variant with the parent folder name of that track at the start of each entry, the reason for this is because some tracks name in ui_track.json is simple "2022" or "GP" which is not understandable so I added the parent folder name to add more context to the name.

Like with the Car list, under the head there is a mapping list so that when you select a track we can get the Parent & Variant folder names which is used in the Special Event .inii file.

<img width="570" height="654" alt="image" src="https://github.com/user-attachments/assets/0c4a3742-01ae-4921-8ce7-a6d3088364a6" />

### Setting Times
The last part of the form is the "Base Time" and the 3 time boxes underneath it.

This is where you will set the reference time to which the Gold, Silver & Bronze times will be calcualted from. The values for each of these is: 2.5%, 5.0% 7 10.0% and these are done against the "Base Time" you set.

The "Base Time" does need to be in a format of: mm:ss.ms (01:22.231) - the form will not calculate the other times and will show a red error text at the bottom if the "Base Time" is not in the expected format.

<img width="573" height="649" alt="image" src="https://github.com/user-attachments/assets/58262bc4-ed81-45d2-9cd3-8af697b0c5fc" />

Once you have filled in the form then all that is left is to hit the "Generate" button, you will get a pop-up confirming the creation:

<img width="571" height="648" alt="image" src="https://github.com/user-attachments/assets/9c8721b7-7c79-4e78-893e-fec854cb3e23" />

Now if you go into Content Manager --> Challenges --> HOTLAPS, you will now see your new Hotlap event.

<img width="2744" height="491" alt="image" src="https://github.com/user-attachments/assets/8ed5c53a-33bf-4750-8642-675c13ec83ab" />

There can be some minor discrepancies with the times, only out by a few milliseconds and this is just down to how the app is calculating the time and how Assetto Corsa stores time in the .ini file for the Special Event.

## Final Note
As said at the top, this was a personal project to challenge myself with a Python app that uses a GUI. While this app does somewhat work for the most part, there are still some bugs and issues as I cannot cater for every single installation scenario of Assetto Corsa content - so this app works well enough on my installation of Assetto Corsa.
