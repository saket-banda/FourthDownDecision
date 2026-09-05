# app.py
from flask_cors import CORS
from flask import Flask, request, jsonify
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import joblib

# rebuilding the exact model architecture
class FourthDownNet(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64), nn.ReLU(),
            nn.Linear(64, 32), nn.ReLU(),
            nn.Linear(32, 1)
        )
    def forward(self, x):
        return self.net(x)

numeric_cols = ['yardline_100', 'ydstogo', 'score_differential', 'game_seconds_remaining', 'qtr']
feature_cols = numeric_cols + ['go', 'punt', 'field_goal']

# load the trained weights and scaler once, at startup 
model = FourthDownNet(input_dim=len(feature_cols))
model.load_state_dict(torch.load('fourth_down_model.pt'))
model.eval()

scaler = joblib.load('scaler.joblib')

# reuse exact prediction function from the notebook
def predict_all_decisions(yardline_100, ydstogo, score_differential, game_seconds_remaining, qtr):
    base = pd.DataFrame([[yardline_100, ydstogo, score_differential, game_seconds_remaining, qtr]],
                         columns=numeric_cols)
    base_scaled = scaler.transform(base)

    results = {}
    for decision, flags in [('go', [1,0,0]), ('punt', [0,1,0]), ('field_goal', [0,0,1])]:
        row = np.concatenate([base_scaled[0], flags])
        x = torch.tensor(row, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            results[decision] = model(x).item()
    return results

# set up the app and the endpoint
app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # parse incoming JSON into a Python dict

    results = predict_all_decisions(
        yardline_100=data['yardline_100'],
        ydstogo=data['ydstogo'],
        score_differential=data['score_differential'],
        game_seconds_remaining=data['game_seconds_remaining'],
        qtr=data['qtr']
    )
    recommended = max(results, key=results.get)  # whichever decision has the highest expected value

    return jsonify({
        "expected_values": results,
        "recommended": recommended
    })

# run app
if __name__ == '__main__':
    app.run(debug=True, port=5000)