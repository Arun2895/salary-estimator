# 💼 AI Salary Estimator

This project provides an intelligent salary estimation system that goes beyond basic averages by combining machine learning predictions with real-world heuristics. It helps users understand their market value based on multiple factors such as role, experience, location, and skillset. The system incorporates fuzzy matching to handle imperfect inputs and applies skill-based adjustments to reflect real-world demand. In addition to predictions, the application features an interactive dashboard that visualizes market trends, salary distributions across locations and career growth patterns. This enables users to not only estimate salaries but also gain deeper insights into industry dynamics for better decision making.

<br>
<img width="800" height="400" alt="Screenshot 2026-04-19 170106" src="https://github.com/user-attachments/assets/4c00dc20-870c-4be9-b825-e4158b9e650a" />

<br>

<img width="800" height="400" alt="Screenshot 2026-04-19 161242" src="https://github.com/user-attachments/assets/758bbbe4-afe6-46a6-ba4b-29175d3cc688" />




## 🚀 Features

* 📊 **Salary Prediction** using Random Forest
* 🔍 **Fuzzy Matching** for role inputs (handles typos)
* 🧠 **Skill-Based Adjustment** for realistic estimates
* 📈 **Market Insights** (salary trends & growth)
* 🎨 **Modern UI** with Streamlit + Glassmorphism



## 🛠 Tech Stack

* **Frontend:** Streamlit
* **ML:** Scikit-learn (Random Forest)
* **Data:** Pandas, NumPy
* **Fuzzy Logic:** TheFuzz
* **Model Storage:** Joblib



## 📂 Structure

```bash
app.py              # Main app
data/               # Dataset
model/              # Model + training notebook
utils/              # Preprocessing & fuzzy logic
.streamlit/         # UI config
```


## ⚙️ Run Locally

```bash
git clone https://github.com/your-username/salary-estimator.git
cd salary-estimator
pip install -r requirements.txt
streamlit run app.py
```



## 📌 Notes

* Model file is excluded (size limit)
* Retrain via `train_model.ipynb`


