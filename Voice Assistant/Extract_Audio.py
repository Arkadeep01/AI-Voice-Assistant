import librosa
import numpy as np

def extract_audio(file_path):
    audio, sample_rate = librosa.load(file_path)
    #MFCCs represent the short-term power spectrum of a sound
    sound = librosa.feature.mfcc(y=audio,sr=sample_rate,n_mfcc=40)
    processed = np.mean(sound.T, axis=0)
    return processed