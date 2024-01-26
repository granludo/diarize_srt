# diarize_srt

Identifies the diferent sepakers in a recording and labels them on a SRT file.

By Marc Alier @granludo hhtps://wasabi.essi.upc.edu/ludo

# About Diarize SRT 

These scripts are designed to perform speaker diarization on recorded conversations. Speaker diarization is the process of partitioning an audio stream into segments according to which speaker is talking. Once the speakers in a conversation are identified, this set of scripts also incorporates the identified speaker information into an SRT (SubRip Subtitle) file. SRT files are used to provide subtitles or captions along with video or audio files. By using these scripts, you can effectively analyze a recorded conversation, determine who is speaking at what times, and then embed this information into the subtitles of the recording. This is particularly useful for creating more informative and accessible audio-visual content, where it's not just the spoken words that are captioned, but also the information about who is speaking them
## TL DR

* This is a small set of python scripts that will allow you to diarize sepakers in a recorded conversation and include the speaker information into a SRT file.

Clone the repo
``
    git clone git@github.com:granludo/diarize_srt.git
``

On ../apis.yaml put your Huggingace token
``
    api:
        huggingface_token: "your_huggingface_token_here"
``
``
python3 diarize.py inputfile.wav outputfile.txt
``

``
python3 diarize_srts.py diarization_file.txt srt_file.srt output_file.srt
``

## Requirements

* We asume you have your audio .wav files and that using OpenAi's "Whisper" or another transcription 
model or app you have your .srt files.
* You nee to install https://github.com/pyannote/pyannote-audio  in your system. And accept the conditions at their hugginface page. https://huggingface.co/pyannote/speaker-diarization-3.1 https://huggingface.co/pyannote/segmentation-3.0 
* You need a Huggingface API token https://huggingface.co/settings/tokens. It should be on a ../apis.yaml , relative to the directory where you put this project. The yaml file should have this format
``
    api:
        huggingface_token: "your_huggingface_token_here"
``

### Installation

Clone the repo
``
    git clone git@github.com:granludo/diarize_srt.git
``
Install requiremenmts - whatch out for M processors users and Cuda setup on the pytorch section. 

``
pip install -r requirements.txt
``

Make sure you have python 3.10 or above installed. Using Anaocnda or another package manager is advided.

### Install pytoch. 
If you are on a M1,M2 or M3 processor you can go to https://developer.apple.com/metal/pytorch/ .
If you are on a CUDA device, make sure the proper pytorch is installed, and  uncomment the lines 48 and 49 on diarize.py and comment the lines 52 and 53.


Install the required packages
``
pip install -r requirements.txt
``

### Run diarization

``
python3 diarize.py inputfile.wav outputfile.txt
``

This will get you a .txt file with contents like this:
``
start=4.1s stop=9.2s speaker_SPEAKER_01
start=11.2s stop=11.8s speaker_SPEAKER_01
start=12.5s stop=13.4s speaker_SPEAKER_01
start=15.5s stop=20.6s speaker_SPEAKER_01
start=21.1s stop=23.8s speaker_SPEAKER_02
start=24.3s stop=27.6s speaker_SPEAKER_02
start=28.9s stop=29.9s speaker_SPEAKER_01
start=30.0s stop=34.2s speaker_SPEAKER_01
start=35.4s stop=37.1s speaker_SPEAKER_01
start=40.2s stop=47.8s speaker_SPEAKER_01
start=51.6s stop=53.4s speaker_SPEAKER_01
start=53.6s stop=72.3s speaker_SPEAKER_05
start=72.9s stop=73.8s speaker_SPEAKER_05
``

For batch operations you can do
``
bash diarize.sh origin_directory output_directory
``
And go grab a cofee.

Now using a text editor and a nice search and replace you can replace "speaker_SPEAKER_01" for "Speaker Name Here".

### Apply diarization to SRT files

A SRT file is a standard subtitles file that you can get from a transcription model like OpenAi's Whisper.

``
python3 diarize_srts.py diarization_file.txt srt_file.srt output_file.srt
``

### Remove all speakers but one

This script is for a special case, supose you want the trasncription of a lecture, for lecture notes or 
a RAG system or something. And you need to keep only the things that ONE speaker says. This have you covered.

``
python3 remove_speakers.py diarization_file.txt srt_file.srt output_file.srt speaker_to_keep
``

