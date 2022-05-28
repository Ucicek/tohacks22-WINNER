from socket import timeout
import PySimpleGUI as sg
import time


"""
    Demo - Fill a listbox with list of files FilesBrowse button
    This technique can be used to generate events from "Chooser Buttons" like FileBrowse, FilesBrowse
    FolderBrowser, ColorChooserButton, Calendar Button
    Any button that uses a "Target" can be used with an invisible Input Element to generate an
    event when the user has made a choice.  Enable events for the invisible element and an event will
    be generated when the Chooser Button fills in the element
    This particular demo users a list of chosen files to populate a listbox
"""


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

window = sg.Window('Window Title', layout, auto_size_buttons=False, grab_anywhere=True)
current_time = 0
start_time = int(round(time.time() * 100))
running = False

# event loop
while True:
    event, values = window.read(timeout=100)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    
    if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Close':        # ALWAYS give a way out of program
        break
    if not running and event == 'Start':
        running = True
        start_time = int(round(time.time() * 100))
    
    if running:
        t = int(round(time.time() * 100))
        current_time = t - start_time 

        # add the live audio processing code below
        pass
    if event == "Submit":
        print(values["-IN-"])
        running = False
        current_time = 0

        # add the mp3 processing code below
        pass

    window['text'].update(
        '{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
        (current_time // 100) % 60,
        current_time % 100)
    )
window.close()