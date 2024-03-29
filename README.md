# Brain Dump - Thought to text

Goal: feature extraction for signals that correlate brain activity with typing words/sentences on keyboard

Approach:

Experiment
- Start an lsl stream
    (device instructions)
    - muse
        - `pip install muselsl`
        - `muselsl stream`
    - neurosity (notion 1,2 & crown)
        I think the lsl stream is always active once devices are on
    (eventually want to use brainflow for this)

- Prompt a word and have user type it
    - `python.exe collect.py session00x`
    
- Record raw eeg epoch as user is typing
  - Python Keylogger with timestamps - https://github.com/tamaramueller/keylogger

    Data shuold look like this ![](./keylogger_screenshots.png)


![Experiment Screenshot_0](./assets/demo_training_experiment_prompt.jpg)
![Experiment Screenshot](./assets/demo_training_experiment.jpg)

![FFT for word on single channel with many samples](./assets/demo_fft_for_word_on_single_chan_many_samples.png)

## Preprocessing Data

- choosing samples
    - find timestamp for every valid word entry in keystroke data
    - filter eeg data with keystroke data for every word sample
    - pick each entry for every sample

- filtering frequency
    - use filtering methods in mne study template
        - https://github.com/mne-tools/mne-study-template/blob/master/scripts/preprocessing/01-import_and_maxfilter.py
        - https://github.com/mne-tools/mne-study-template/blob/master/scripts/preprocessing/02-frequency_filter.py
    - apply a band pass filter to remove harmoinic noise

- selecting what channels to use
    - visualize fft for a single sample and pick the channel with the highest (but not weirdest)
        - x axis bins (0-55), y- axis voltage
        - plot all channels together
    - after picking a single channel, you're ready to send fft data for that to gpt

- feeding data to gpt
    - get combined df for typing matchings (across different words)
        - loop through word prompts
        - apply current preprocessing and have a data set that contains "word prompt" & fft string pairs
        - use 60:40 split for training and testing
    
    - send fft prompt for channel to gpt "wordprompt: easy; fft: [rrrbs,bsbssbsbs]"
	    - select frequencies between 2-50Hz

    - measure accuracy, precision & recall for examples

(misc)
- record more experiments and performance
    - do the experiment a few different times on different days
- clean up [scratch.ipynb](./scratch.ipynb) into a shareable script
- consider transfer learning if gpt doesnt work well

Inference
how do we do inteference realtime on notion
   - https://github.com/neurosity/eeg-pipes
   - https://github.com/neurosity/brainwaves-node/blob/master/lowAlpha.js
    
## Roadmap
7.08.2022
    - the goal for today is:
        - switch to brainflow for collecting data
        - run the collect.py and make sure
            - timestamp of prompts
            - csv data with keypress is included

8.08.2022
    - get back to feature analyis
        - generate an input matrix that can be fed into a classifier
        - try multiple classifiers and measure