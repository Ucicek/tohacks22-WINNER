import json
import base64
import asyncio
import requests
import websockets
from time import sleep
from datetime import datetime
from configure import assemblyai_auth_key, cohere_auth_key

api_key = cohere_auth_key

import wave
import pyaudio
import cohere
from cohere.classify import Example

FRAMES_PER_BUFFER = 3200 #started at 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()
co = cohere.Client(f'{api_key}')

def record_segment(len, idx=0):
    """
    Records a segment of data, stores the wav file.

    :param len: length of recording in seconds
    :param idx: idx of your recording for filepath
    :return filepath: path to mp3 file
    """

    #starts recording
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=FRAMES_PER_BUFFER
    )

    frames = []
    print("Recording has started")

    for i in range(0, int(RATE / FRAMES_PER_BUFFER * len)):
        data = stream.read(FRAMES_PER_BUFFER)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()

    file_name = str(idx) + '_' + str(datetime.now()).replace(' ', '_').replace(':', '_') + '.wav'

    # Save the recorded data as a WAV file
    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return file_name

def read_file(filename):
    """
    Reads audio file and returns generator for transcription request.

    :param filename: string filepath to audio file
    :return data: generator with audio data
    """

    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(5242880)
            if not data:
                break
            yield data

def transcribe_segment(fpath):
    """
    Transcribes segment of data into text. Slices into phrases as well.

    :param fpath: path to .wav file where audio has been recorded
    :return transcription: dictionary object of transcribed data
    """

    headers = {
       "authorization": assemblyai_auth_key,
       "content-type": "application/json"
    }
    
    # Request upload
    upload_endpoint = 'https://api.assemblyai.com/v2/upload'
    upload_response = requests.post(
                                    upload_endpoint,
                                    headers=headers, 
                                    data=read_file(fpath)
                                    )
    print('Audio file uploaded')
    
    # Request transcription
    transcript_endpoint = "https://api.assemblyai.com/v2/transcript"
    transcript_request = {'audio_url': upload_response.json()['upload_url']}
    transcript_response = requests.post(transcript_endpoint, 
                                        json=transcript_request, 
                                        headers=headers)
    print('Transcription Requested')

    # Set up polling and poll till completion
    polling_response = requests.get(transcript_endpoint+"/"+transcript_response.json()['id'], headers=headers)
    x = 0
    while polling_response.json()['status'] != 'completed':
       sleep(1)
       x += 1
       polling_response = requests.get(transcript_endpoint+"/"+transcript_response.json()['id'], headers=headers)

    print("Needed " + str(x) + " seconds to process.")

    full_text = str(polling_response.json()["text"])
    full_text = full_text.replace('?', '.').replace('!', '.')
    phrases = full_text.split('.')
    corrected_phrases = []

    for i, phrase in enumerate(phrases):
        isCorr = False
        for char in phrase:
            if char != ' ':
                isCorr = True
        
        if(isCorr):
            corrected_phrases.append(phrase)

    print(phrases)

    return {'text' : str(polling_response.json()["text"]), 'phrases' : corrected_phrases}

def predict_danger(input):
    """
    Predicts danger level of inputs. 

    :param input: list of input phrases
    :return output: output predictions
    """

    classifications = co.classify(
        model='medium',
        taskDescription='',
        outputIndicator='',
        inputs=dict_result['phrases'],
        examples=[Example("How did you manage to fail the exam.", "Negative"), Example("You do not understand", "Negative"), Example("Can you not do that", "Negative"), Example("You are so bad", "Negative"), Example("You always give up ", "Negative"), Example("Harrison Ford is 6’1”.", "Neutral"), Example("Yesterday, he traded in his Android for an iPhone.", "Neutral"), Example("Where are you from?", "Neutral"), Example("Are you okay?", "Neutral"), Example("Please help me", "Neutral"), Example("I don’t understand you", "Neutral"), Example("How are you doing?", "Neutral"), Example("What is that", "Neutral"), Example("Can you give me that?", "Neutral"), Example("I can do that", "Neutral"), Example("This a sofa", "Neutral"), Example("This is Jackso n", "Neutral"), Example("He is a guy", "Neutral"), Example("She is a girl", "Neutral"), Example("I am feeling good today.", "Positive"), Example("In three years, everyone will be happy.", "Positive"), Example("Have a good day! ", "Positive"), Example("You are doing very well.", "Positive"), Example("Proud of you!", "Positive"), Example("How can you be so stupid.", "Super Negative"), Example("Don\'t get near me.", "Super Negative"), Example("I hate you.", "Super Negative"), Example("You are sick.", "Super Negative"), Example("You deserve death.", "Super Negative"), Example("Wow, you are super tall.", "Super positive"), Example("Good job on getting 100%.", "Super positive"), Example("You are so talented at this! ", "Super positive"), Example("You are handsome", "Super positive"), Example("I’m behind you 100%.", "Super positive"), Example("Your skirt is so pretty.", "Super positive"), Example("You look great today.", "Super positive"), Example("You’re a fantastic cook.", "Super positive"), Example("You have the best style.", "Super positive"), Example("You are the best", "Super positive"), Example("You are pretty", "Super positive"), Example("I got a 100%", "Super positive"), Example("You are good looking", "Super positive"), Example("I wish I was like you", "Super positive"), Example("You are cute", "Super positive"), Example("I love my parents", "Super positive"), Example("You are the nicest person ever", "Super positive"), Example("I love my friends", "Super positive"), Example("I feel very nice", "Super positive"), Example("I am feeling very good", "Super positive"), Example("I like your dog", "Super positive")])

    dict_classifications = {}

    for classification in classifications:
        label = classification.prediction
        confidence_score = 0.0
        for conf in classification.confidence:
            if conf.label == label:
                confidence_score = conf.confidence

        dict_classifications.update({classification.input : (label, confidence_score)})

    return dict_classifications
    

fname = record_segment(20, 0)
dict_result = transcribe_segment(fname)
print(dict_result['text'])
print(dict_result['phrases'])

dict_classifciation = predict_danger(dict_result['phrases'])
print(dict_classifciation)

