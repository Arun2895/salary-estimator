import pandas as pd
import numpy as np
import joblib
import sys, os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from utils.preprocess import compute_skill_score

df = pd.read_csv(os.path.join(ROOT, 'data', 'salary_prediction_dataset.csv'))
df = df.fillna('')
print(f"Loaded {len(df):,} rows, {df['job_title'].nunique()} unique roles")

df['skill_score'] = df.apply(compute_skill_score, axis=1)

le_job      = LabelEncoder()
le_location = LabelEncoder()
df['job_title_encoded'] = le_job.fit_transform(df['job_title'])
df['location_encoded']  = le_location.fit_transform(df['location'])

features = ['job_title_encoded', 'location_encoded', 'experience_years', 'skill_score']
X     = df[features].reset_index(drop=True)
y_min = df['salary_min_lpa'].reset_index(drop=True)
y_max = df['salary_max_lpa'].reset_index(drop=True)

X_tr, X_te, ym_tr, ym_te, yM_tr, yM_te = train_test_split(
    X, y_min, y_max, test_size=0.2, random_state=42
)

print("Training min-salary model...")
min_model = RandomForestRegressor(n_estimators=200, min_samples_leaf=3, random_state=42, n_jobs=-1)
min_model.fit(X_tr, ym_tr)

print("Training max-salary model...")
max_model = RandomForestRegressor(n_estimators=200, min_samples_leaf=3, random_state=42, n_jobs=-1)
max_model.fit(X_tr, yM_tr)

mae_min = mean_absolute_error(ym_te, min_model.predict(X_te))
r2_min  = r2_score(ym_te, min_model.predict(X_te))
mae_max = mean_absolute_error(yM_te, max_model.predict(X_te))
r2_max  = r2_score(yM_te, max_model.predict(X_te))

print(f"\n--- PERFORMANCE (held-out test set) ---")
print(f"Min Salary Model : MAE = {mae_min:.2f} LPA  |  R2 = {r2_min:.3f}")
print(f"Max Salary Model : MAE = {mae_max:.2f} LPA  |  R2 = {r2_max:.3f}")

# Retrain on full data before saving
min_model.fit(X, y_min)
max_model.fit(X, y_max)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'salary_model.pkl')
joblib.dump({
    'min_model':   min_model,
    'max_model':   max_model,
    'le_job':      le_job,
    'le_location': le_location,
}, out_path)
print(f"Models saved -> {out_path}")
