# 💼 AI Salary Estimator

A machine learning-powered web app that predicts salary ranges for tech roles using role, experience, location, and skills.



## 🚀 Features

* 📊 **Salary Prediction** using Random Forest
* 🔍 **Fuzzy Matching** for role inputs (handles typos)
* 🧠 **Skill-Based Adjustment** for realistic estimates
* 📈 **Market Insights** (salary trends & growth)
* 🎨 **Modern UI** with Streamlit + Glassmorphism

---

## 🛠 Tech Stack

* **Frontend:** Streamlit
* **ML:** Scikit-learn (Random Forest)
* **Data:** Pandas, NumPy
* **Fuzzy Logic:** TheFuzz
* **Model Storage:** Joblib

---

## 📂 Structure

```bash
app.py              # Main app
data/               # Dataset
model/              # Model + training notebook
utils/              # Preprocessing & fuzzy logic
.streamlit/         # UI config
```

---

## ⚙️ Run Locally

```bash
git clone https://github.com/your-username/salary-estimator.git
cd salary-estimator
pip install -r requirements.txt
streamlit run app.py
```

---

## 📌 Notes

* Model file is excluded (size limit)
* Retrain via `train_model.ipynb`


