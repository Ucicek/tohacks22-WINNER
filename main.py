# importing the libraries
import os
import PySimpleGUI as sg
import time
import pyaudio
import cohere
from cohere.classify import Example
import ai_integration.process as pr

FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

api_key = 'KZyl9VEB48EaDmsfJFOA4mMS53AsYrsBCZTSK7vg'

p_obj = pyaudio.PyAudio()
co = cohere.Client(f'{api_key}')

# layout code for the GUI itself
layout = [  
    [
        sg.Text('words',  
            font=('Helvetica', 20), 
            justification='center', 
            key='text'
        )
    ],
    [
        sg.Text("Choose a folder: "), 
        sg.Input(key="-IN2-" ,change_submits=True), 
        sg.FileBrowse(key="-IN-")
    ],
    [ sg.Button("Submit") ],
    [
        sg.Button('Start', button_color=('white', '#007339')),
        sg.Exit('Close', button_color=('white', '#001480')),
    ],
             
]

# creating the window object
window = sg.Window('Window Title', layout, auto_size_buttons=False, grab_anywhere=True)

# variables for the event loop
current_time = 0
start_time = int(round(time.time() * 100))
running = False

# event loop
while True:
    # window reading values
    event, values = window.read(timeout=100)

    # breaking the loop
    if event in (sg.WIN_CLOSED, 'Exit') or event == sg.WIN_CLOSED or event == 'Exit' or event == 'Close':        # ALWAYS give a way out of program
        break

    # variables inside the loop
    if not running and event == 'Start':
        running = True
        start_time = int(round(time.time() * 100))
    
    # live processing started
    if running:
        t = int(round(time.time() * 100))
        current_time = t - start_time 

        fname = pr.record_segment(20, p=p_obj, idx=0)
        dict_result = pr.transcribe_segment(fname)
        dict_classifciation = pr.predict_danger(dict_result['phrases'], co)
        if os.path.exists(fname):
            os.remove(fname)

        print(dict_classifciation)

    # submitting a .wav file
    if event == "Submit":
        print(values["-IN-"])
        running = False
        current_time = 0

        # add the mp3 processing code below
        pass

    # updating the values interface
    window['text'].update(
        '{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
        (current_time // 100) % 60,
        current_time % 100)
    )
window.close()