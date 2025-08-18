from transformers import VitsModel, AutoTokenizer
import torch
import soundfile as sf
import os

MODEL_DIR = os.path.join("models", "mms-tts-eng")
TEXT = "Hello from MMS TTS. This is a quick audio test."
OUT_PATH = "tts_test.wav"

print("Loading tokenizer/model from:", os.path.abspath(MODEL_DIR))

tok = AutoTokenizer.from_pretrained(MODEL_DIR)
model = VitsModel.from_pretrained(MODEL_DIR)

inputs = tok(TEXT, return_tensors="pt")
with torch.no_grad():
    out = model(**inputs)

wav = out.waveform.squeeze().cpu().numpy()
# MMS TTS VITS outputs 16kHz audio by default
sf.write(OUT_PATH, wav, 16000)
print("Wrote:", os.path.abspath(OUT_PATH), "samples:", wav.shape[0])
