from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
import os
import wave
import pylab
import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import openai
from openai.error import RateLimitError
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)
openai.api_key = "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"

def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate

def graph_spectrogram(wav_file, save_path):
    sound_info, frame_rate = get_wav_info(wav_file)
    pylab.figure(num=None, figsize=(19, 12))
    pylab.subplot(111)
    plt.axis("off")
    #pylab.title('spectrogram of %r' % wav_file) 
    pylab.specgram(sound_info, Fs=frame_rate) #return
    pylab.savefig(save_path)

def read_image(filename):
    img = load_img(filename)
    img = img_to_array(img)
    img = np.resize(img, (256,256,3))
    img = np.expand_dims(img, axis=0)
    return img

def predict(img):
    model = load_model("speech_disorders.h5")
    pred = model.predict(img)
    val = np.argmax(pred)
    if val == 4:
        return "Stutter - frequent problems with the normal fluency and flow of speech"
    if val == 3:
        return "Rhotacism - difficulty pronouncing the sound 'R'"
    if val == 2:
        return "Dysarthria - weakness in the muscles used for speech"
    if val == 1:
        return "Apraxia - disorder affecting the brain pathways involved in producing speech."
    else:
        return "NONE"

@app.route("/")
def home():
   return render_template("form_screen.html")

@app.route("/predict", methods=["GET", "POST"])
def get_pred():
    if request.method == "POST":
      rand = np.random.randint(0,100)
      #path = f"./images/spec{rand}.png"
      f = request.files['file']
      path = "static/spectrogram.png"
      graph_spectrogram(f, path)
      real_path = f"images\spec{rand}.png"
      img = read_image("static\spectrogram.png")
      pred = predict(img)
      current = datetime.now()
      time = f'{current.month}/{current.day}/{current.year}'
      return render_template("new.html", condition=pred)
    else:
        img = read_image("static\spectrogram.png")
        pred = predict(img)
        return render_template("new.html", condition=pred)
    
@app.route('/gpt4', methods=['GET,', 'POST'])
def gpt4():
    user_input = request.args.get('user_input') if request.method == 'GET' else request.form['user_input']
    messages = [{"role": "user", "content": user_input}]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        content = response.choices[0].message["content"]
    except RateLimitError:
        content = "The server is experiencing a high volume of requests. Please try again later."

    return jsonify(content=content)

@app.route("/spectrogram", methods=["POST", "GET"])
def show_spectrogram():
    if request.method == "POST":
        current = datetime.now()
        time = f'{current.month}/{current.day}/{current.year}'
        return render_template("test.html", time=time)

if __name__ == "__main__":
    app.run(debug=True)