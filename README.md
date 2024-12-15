# bayesian-melody-predictor
The project extracted 57,305 Gregorian melodies from the Cantus database, converting them into MIDI pitch sequences. A Gaussian Process Regression (GPR) model was trained using a sliding window approach to predict 8-note continuations from 32-note inputs. The model achieved 80.58% accuracy on Gregorian test sets and 21.82% on modern pop melodies in zero-shot testing.

# Running Guide
## Environment Setup
```
# Create a new conda environment
conda create -n bayesian-melody-predictor python=3.10.15
conda activate bayesian-melody-predictor

# Install dependencies
pip install -r requirements.txt
```
## Running the Model
```
cd [parent folder of the project]/bayesian-melody-predictor

python test_gaussian_process.py
```

# Evaluation Mechanism
The test set has one 32-note input and 10 8-note options. The model will predict a 8-note continuation from the 32-note input. Then compare the predicted 8-note continuation with the 10 8-note options. The option which has the highest similarity with the predicted 8-note continuation will be considered as the correct answer.

# Results
| Dataset | Accuracy |
| --- | --- |
| Gregorian Chant | 80.58% |
| Modern Pop | 21.82% |