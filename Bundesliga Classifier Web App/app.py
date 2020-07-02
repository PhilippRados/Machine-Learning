import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('bl_clf.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():
    #Code for receiving input and manipulating it

    inputs = np.array([str(x) for x in request.form.values()])
    pos_t = [0,2]
    pos_o = [1,3]
    teams = [int(i) for i in inputs[pos_t]]
    odds = [float(i) for i in inputs[pos_o]]

    if teams[0] == teams[1]:
        output = "You can't choose the same team twice"
    else:
        X = [(teams + odds)]
        prediction = model.predict(X)
        if prediction == [1]:
            output = "Home-team will win this one"
        elif prediction == [2]:
            output = "Away-team will win this one"
        elif prediction == [0]:
            output = "This will be a draw"

    return render_template('predict.html', prediction_text=output)


if __name__ == "__main__":
    app.run(debug=True)