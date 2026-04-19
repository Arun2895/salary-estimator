# Salary Predictor

A simple machine learning project to predict salaries based on years of experience.

## Project Structure
```
salary-predictor
│
├── data
│   └── salaries.csv         # Raw dataset
│
├── model
│   ├── train_model.py       # Training script
│   └── salary_model.pkl     # Trained weights (generated)
│
├── app
│   └── app.py               # Streamlit dashboard
│
├── utils
│   ├── preprocess.py        # Preprocessing helpers
│   └── fuzzy_logic.py       # Fuzzy logic salary estimation
│
└── requirements.txt         # Dependencies
```

## How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Train the Model**:
   ```bash
   python model/train_model.py
   ```

3. **Launch the Dashboard**:
   ```bash
   streamlit run app/app.py
   ```
