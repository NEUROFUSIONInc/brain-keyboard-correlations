# Brain Dump - Thought to text

Goal: Recognize words in my thoughts and be able to write them as text in realtime

Apporach:

Experiment
![Experiment Screenshot](./assets/demo_training_experiment.jpg)

- Prompt a word and have user type it
- Record raw eeg epoch as user is typing
    - CuriaRecorder - to record the data
    - CuriaIO-rc3 - to log key data
    `curiarecorder.exe -c * -r 2 test.csv`

Preprocessing Data

- choosing samples
    - pick each entry for every sample

- selecting what channels to use
    - visualize on fft result
    - x axis bins (0-55), y- axis voltage
    - plot all channels together

- feeding data to gpt
    - get combined df for typing matchings (across different words)
    - get fft for the selected channels
    - send fft prompt for channel to gpt "wordprompt: easy; fft: [rrrbs,bsbssbsbs]"
	    - cut off at 50Hz ( stop index at 50 )
   	    - for high gamma data ( replace value 55-65 to zero )

Inference
- Send words & examples to gpt3
- See if it an recognize with new data