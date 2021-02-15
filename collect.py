import os
import sys
import random
import time
import threading

from pylsl import StreamInlet, resolve_stream
import PySimpleGUI as sg
import pandas as pd

WORDS = ("python", "jumble", "easy", "difficult", "answer",  "xylophone")
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = BASE_DIR + "\\data"


prompt_entries = [] # format of each entry is timestamp, wordprompt

def get_prompt():
    # write the words being chosen into a list with timestamps
    # write to csv afterwards
    prompt = random.choice(WORDS)
    prompt_entries.append([time.time(), prompt])
    return prompt

def display_words():
    # define experiment layout
    layout = [
        [sg.Text(get_prompt(), key="wordprompt", size=(50, 1), justification='center', font=("Helvetica", 25))], 
        [sg.Input(key='wordinput', change_submits=True, size=(50,1), justification='center', font=("Helvetica", 25))], 
    ]

    # Create the window
    window = sg.Window("braindump", 
                        layout, auto_size_text=True, finalize=True,
                        text_justification='center')
    window.maximize()
    sg.popup("Please type the prompted word in text area", title='braindump')

    # Create an event loop
    while True:
        event, values = window.read()

        # End program if user closes window or
        # presses the OK button
        if event == sg.WIN_CLOSED:
            break

        # if the input value is equal to 
        if window['wordinput'].get() == window['wordprompt'].get():
            sg.popup("Word match! Displaying next word in 3", auto_close = True, auto_close_duration = 3)

            # empty input field
            window['wordinput'].update('')

            # generate next prompt
            window['wordprompt'].update(get_prompt())

    window.close()

def activate_lsl_stream():
    try:
        # first resolve an EEG stream on the lab network
        print("looking for an EEG stream...")
        streams = resolve_stream('type', 'EEG')
        # create a new inlet to read from the stream
        inlet = StreamInlet(streams[0])
        print("EEG Stream created")
    except KeyboardInterrupt as e:
        print("Ending program")
        raise e

def write_outputs_to_csv(sessionname):
    # get write the time list to a csv
    prompt_df = pd.DataFrame(prompt_entries)
    prompt_df.to_csv(DATA_DIR + '\\{}-wordprompts.csv'.format(sessionname),
                    index=False, header=['timestamp', 'wordprompt'])

def start_curia_stream():
    pass

if __name__ == '__main__':
    activate_lsl_stream()
    display_words()
    write_outputs_to_csv(str(int(time.time())))