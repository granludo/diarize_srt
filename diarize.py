# For Mac M processors 
# pip3 install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/nightly/cpu
# https://developer.apple.com/metal/pytorch/
# https://developer.apple.com/metal/mps/
# https://huggingface.co/pyannote/speaker-diarization-3.1

import yaml
import torch
import sys
import os
from pyannote.audio import Pipeline


def test_torch():
    """ Use torch to test if MPS is available. """
    if torch.backends.mps.is_available():
        mps_device = torch.device("mps")
        x = torch.ones(1, device=mps_device)
        print (x)
    else:
        print ("MPS device not found.")



def get_huggingface_token(yaml_file_path="../apis.yaml"):
    """
    # ample_apis.yaml

    api:
        huggingface_token: "your_huggingface_token_here"

    """

    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)
        # Accessing the nested 'huggingface_token' under 'api'
        return data['api']['huggingface_token'] if 'api' in data and 'huggingface_token' in data['api'] else None


def diarize(inputfile,outputfile):

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=get_huggingface_token(),
    )

    # send pipeline to GPU (when available)
    # pipeline.to(torch.device("cuda"))
    # print("Using CUDA GPU")

    # send pipeline to MPS (when available)
    pipeline.to(torch.device("mps"))
    print("Using MPS GPU (Apple M processors)")

    # apply pretrained pipeline
    diarization = pipeline(inputfile)

    # print the result
    with open(outputfile, "w") as f:
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}", file=f)
            print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 diarize.py inputfile outputfile")
        sys.exit(1)
    input_audio = sys.argv[1]
    outputfile = sys.argv[2]
   # Check if the input file exists and is a .wav file
    if not os.path.exists(input_audio):
        print(f"Error: The file {input_audio} does not exist.")
        sys.exit(1)
    if not input_audio.lower().endswith('.wav'):
        print("Error: The input file is not a .wav file.")
        sys.exit(1)
    print("Diarizing file {input_audio} to {outputfile}")    
    diarize(input_audio,outputfile)
    print("*************** Done")
if __name__ == "__main__":
    main()
