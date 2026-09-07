# 4th Down Decision Model

A full-stack tool that estimates the expected point value of fourth down options (going for it, punting, or kicking a field goal) on any 4th down situation. Designed to compare against real coaching decisions.

## Overview

By using 10 seasons (~40K plays) of NFL play data, this project trains a PyTorch neural network to predict the expected points added (EPA) of a 4th-down play, given the game situation and the decision made. Because a coach only ever makes one choice per real play, the decision itself is treated as a model input rather than an output. This enables a counterfactual comparison: the same situation can be run through the model three times, once per decision, to see what each option would be expected to yield.

The model is served through a Flask API and a React dashboard, where users can enter any game situation to see a comparison of all three decisions.

## Key takeaways

- **~40K historical 4th-down plays** across 10 NFL seasons used for training and evaluation
- **Counterfactual inference design**: decision-as-input architecture allows direct comparison of all three options for a single play, sidestepping the fact that only one decision is ever observed per real play
- **Early stopping** based on validation loss to prevent overfitting, improving on a mean-prediction baseline
- **Full-stack deployment**: Flask REST API + React dashboard for real-time, interactive predictions
- Backtesting against real historical decisions surfaced a known limitation in single-play EPA as a target variable — see [Limitations](#limitations--future-work) below

## Tech stack

`Python` · `pandas` · `PyTorch` · `Flask` · `React` · `nflreadpy`

## How it works

1. **Data pipeline** — pulls and cleans 10 seasons of play-by-play data, filters to 4th downs, labels each play's actual decision
2. **Model** — a neural network trained on situation + decision → EPA, using early stopping to select the best-generalizing checkpoint
3. **API** — a Flask endpoint loads the trained model and scaler, and returns expected values for all three decisions given any input situation
4. **Dashboard** — a React frontend for entering a game situation and viewing the model's recommendation

## Running it locally

**Requirements:** Python 3.10+, Node.js, conda (recommended)

**1. Clone the repo**
```bash
git clone https://github.com/saket-banda/FourthDownDecision.git
cd FourthDownDecision
```

**2. Set up the backend**
```bash
cd backend
conda create -n fourthdown python=3.11
conda activate fourthdown
pip install flask flask-cors torch pandas scikit-learn joblib
python app.py
```
Runs at `http://127.0.0.1:5000`

**3. Set up the frontend** (in a separate terminal)
```bash
cd frontend
npm install
npm run dev
```
Runs at `http://localhost:5173` — open this in your browser

## Limitations & future work

- The model was trained on single-play EPA, which underrepresents the deferred field-position value of punting — a planned improvement is switching to win-probability-added (WPA) as the target
- Predictions in rarely-observed regions of the input space (e.g. long field goal attempts from deep in a team's own territory) can be unreliable due to limited training examples in those situations
- Future additions: timeouts remaining, home/away, team strength adjustments
