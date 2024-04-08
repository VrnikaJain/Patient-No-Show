from flask import Flask, render_template, request
import pickle
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load the pre-trained model
model=pickle.load(open('model.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extracting inputs from the form
    gender = int(request.form['gender'])
    age = int(request.form['age'])
    scholarship = int(request.form['scholarship'])
    hypertension = int(request.form['hypertension'])
    diabetes = int(request.form['diabetes'])
    alcoholism = int(request.form['alcoholism'])
    handicap = int(request.form['handicap'])
    sms_received = int(request.form['sms_received'])
    
    # Making prediction
    prediction = model.predict([[gender, age, scholarship, hypertension, diabetes, alcoholism, handicap, sms_received]])[0]
    if prediction == 1:
        result = 'Show'
    else:
        result = 'No-show'

    # Counting predictions
    predictions = model.predict_proba([[gender, age, scholarship, hypertension, diabetes, alcoholism, handicap, sms_received]])
    show_percentage = round(predictions[0][1] * 100, 2)
    no_show_percentage = round(predictions[0][0] * 100, 2)

    return render_template('index.html', prediction=result, show_percentage=show_percentage, no_show_percentage=no_show_percentage)

if __name__ == '__main__':
    app.run(debug=True)
