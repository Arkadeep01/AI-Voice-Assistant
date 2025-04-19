import joblib
from Extract_Audio import extract_audio

model = joblib.load("emotion_model.pkl")

def predict_emotion(file_path):
    features = extract_audio(file_path)
    emotion = model.predict([features])[0]
    return emotion