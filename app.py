import streamlit as st
import joblib
import os
import pandas as pd
import numpy as np
import plotly.express as px
from rapidfuzz import process, fuzz

from utils.preprocess import compute_skill_score
from utils.fuzzy_logic import get_skill_level

# --- Page config --------------------------------------------------------------
st.set_page_config(
    page_title="Salary Estimator & Market Analytics",
    layout="wide"
)

# --- CSS ----------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

.stApp { background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%); min-height: 100vh; }

/* - Tabs - */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,0.04);
    padding: 6px;
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    color: #94a3b8;
    border-radius: 10px;
    padding: 8px 20px;
    font-weight: 600;
    font-size: 0.9rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
}

/* - Cards - */
.glass-card {
    padding: 2rem;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    margin-bottom: 1.5rem;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0,0,0,0.4);
}

/* - Section labels - */
.section-label {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #6366f1;
    margin-bottom: 0.4rem;
}

/* - Text inputs - */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.07) !important;
    border: 1.5px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.2s ease !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.2) !important;
}
.stTextInput > div > div > input::placeholder { color: #64748b !important; }

/* - Selectbox - */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1.5px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: white !important;
}

/* - Fuzzy match hint - */
.fuzzy-match-hint {
    font-size: 0.82rem;
    color: #a5b4fc;
    margin-top: 4px;
    padding: 4px 10px;
    background: rgba(99, 102, 241, 0.1);
    border-radius: 8px;
    border: 1px solid rgba(99, 102, 241, 0.2);
    display: inline-block;
}
.fuzzy-no-match {
    font-size: 0.82rem;
    color: #cbd5e1;
    margin-top: 4px;
    padding: 4px 10px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: inline-block;
}

/* - Radio experience - */
.stRadio > div { gap: 6px !important; flex-wrap: wrap !important; }
.stRadio > div > label {
    background: rgba(255,255,255,0.06) !important;
    border: 1.5px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    padding: 6px 16px !important;
    color: #cbd5e1 !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    font-size: 0.88rem !important;
}
.stRadio > div > label:hover {
    border-color: #6366f1 !important;
    color: white !important;
    background: rgba(99,102,241,0.12) !important;
}
.stRadio > div [aria-checked="true"] + div {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    border-color: transparent !important;
    color: white !important;
}

/* - Skill bubbles - */
.skill-bubbles-wrap { display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0 14px 0; min-height: 36px; }
.skill-bubble {
    display: inline-flex; align-items: center; gap: 6px;
    background: linear-gradient(135deg, rgba(99,102,241,0.3), rgba(139,92,246,0.3));
    border: 1px solid rgba(139,92,246,0.5);
    color: #e0e7ff;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    animation: popIn 0.2s ease;
}
.skill-bubble .x-btn {
    background: rgba(255,255,255,0.15);
    border: none;
    color: white;
    width: 18px; height: 18px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer;
    font-size: 0.7rem;
    font-weight: 700;
    line-height: 1;
}
@keyframes popIn { from { transform: scale(0.7); opacity: 0; } to { transform: scale(1); opacity: 1; } }
.skill-limit-warn { font-size: 0.8rem; color: #ffffff; margin-top: 4px; }

/* - Skill Buttons - */
div[data-testid="stButton"] > button[data-testid="baseButton-secondary"] {
    border-radius: 999px !important;
    padding: 4px 16px !important;
    height: auto !important;
    background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.1)) !important;
    border: 1px solid rgba(139,92,246,0.4) !important;
    color: #e0e7ff !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    width: auto !important;
    display: inline-flex !important;
    box-shadow: none !important;
    margin-right: 8px !important;
}
div[data-testid="stButton"] > button[data-testid="baseButton-secondary"]:hover {
    background: rgba(255,255,255,0.1) !important;
    border-color: rgba(255,255,255,0.3) !important;
    color: white !important;
}

/* - Predict Button - */
div[data-testid="stButton"] > button[data-testid="baseButton-primary"] {
    width: 100%;
    border-radius: 14px;
    height: 3.8rem;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    font-weight: 700;
    font-size: 1.05rem;
    border: none;
    transition: all 0.3s ease;
    letter-spacing: 0.3px;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4);
}
div[data-testid="stButton"] > button[data-testid="baseButton-primary"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 32px rgba(99,102,241,0.55);
}
div[data-testid="stButton"] > button[data-testid="baseButton-primary"]:active { transform: translateY(0px); }

/* - Result card - */
.prediction-range {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.pred-label {
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #94a3b8;
    margin-bottom: 0.5rem;
}
.pred-value {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.company-tag {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 10px 18px;
    background: rgba(255,255,255,0.06);
    color: #e2e8f0;
    border-radius: 12px;
    font-weight: 600;
    margin: 5px 5px 5px 0;
    border: 1px solid rgba(255,255,255,0.1);
    font-size: 0.9rem;
}

/* - Headings - */
h1, h2, h3, h4 { color: white !important; }
p, li { color: #94a3b8; }
.stMarkdown p { color: #94a3b8; }
label { color: #cbd5e1 !important; }
.stAlert { border-radius: 12px !important; }

/* - Metrics - */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
}
[data-testid="metric-container"] label { color: #94a3b8 !important; font-size: 0.85rem !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: white !important; font-weight: 700 !important; }


/* - Footer - */
.footer { text-align: center; color: #334155; font-size: 0.8rem; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.05); }
</style>
""", unsafe_allow_html=True)

# --- Constants ----------------------------------------------------------------
MODEL_PATH = "model/salary_model.pkl"
DATA_PATH  = "data/salary_prediction_dataset.csv"

EXPERIENCE_OPTIONS = [
    "0 yrs (Fresher)", "1 yr", "2 yrs", "3 yrs", "4 yrs", "5 yrs",
    "6 yrs", "7 yrs", "8 yrs", "9 yrs", "10 yrs", "12 yrs",
    "15 yrs", "18 yrs", "20 yrs", "25 yrs", "30 yrs", "35 yrs", "40 yrs"
]
EXP_VALUE_MAP = {
    "0 yrs (Fresher)": 0, "1 yr": 1, "2 yrs": 2, "3 yrs": 3, "4 yrs": 4,
    "5 yrs": 5, "6 yrs": 6, "7 yrs": 7, "8 yrs": 8, "9 yrs": 9,
    "10 yrs": 10, "12 yrs": 12, "15 yrs": 15, "18 yrs": 18,
    "20 yrs": 20, "25 yrs": 25, "30 yrs": 30, "35 yrs": 35, "40 yrs": 40
}

# --- Load model & data --------------------------------------------------------
@st.cache_resource
def load_assets():
    model_data = None
    if os.path.exists(MODEL_PATH):
        model_data = joblib.load(MODEL_PATH)
    df = pd.DataFrame()
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH).dropna()
    return model_data, df

model_data, df_raw = load_assets()

if model_data is None or df_raw.empty:
    st.markdown(
        "<div style='padding: 1rem; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; color: white; text-align: center;'>Missing model or data. Please run model/train_model.py first.</div>",
        unsafe_allow_html=True
    )
    st.stop()

min_model   = model_data["min_model"]
max_model   = model_data["max_model"]
le_job      = model_data["le_job"]
le_location = model_data["le_location"]

KNOWN_JOBS = list(le_job.classes_)

# --- Fuzzy job matcher --------------------------------------------------------
def fuzzy_match_job(query: str, choices: list, threshold: int = 45):
    """Return (best_match, score) or (None, 0) if below threshold."""
    if not query.strip():
        return None, 0
    query_lower = query.lower().strip()
    
    # 1. Exact or prefix match prioritized
    prefix_matches = [c for c in choices if c.lower().startswith(query_lower)]
    if prefix_matches:
        # Return the shortest prefix match 
        best = min(prefix_matches, key=len)
        return best, 100
        
    result = process.extractOne(query, choices, scorer=fuzz.WRatio)
    if result and result[1] >= threshold:
        return result[0], result[1]
    return None, 0

# --- Session state initialisation ---------------------------------------------
if "skills" not in st.session_state:
    st.session_state.skills = []

def submit_skill():
    val = st.session_state.skill_input_val
    if val:
        skill = val.strip().title()
        if skill and len(st.session_state.skills) < 5:
            if skill.lower() not in [s.lower() for s in st.session_state.skills]:
                st.session_state.skills.append(skill)
    # Clear the input
    st.session_state.skill_input_val = ""

def remove_skill(idx: int):
    st.session_state.skills.pop(idx)

# --- Tabs ---------------------------------------------------------------------
tab1, tab2 = st.tabs(["AI Salary Predictor", "Market Analytics"])

# --------------------------------------------------------
#  TAB 1 - PREDICTOR
# --------------------------------------------------------
with tab1:
    st.markdown("<h1 style='margin-bottom:0'>Salary Estimator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b; margin-top:4px; margin-bottom:1.5rem'>AI-powered compensation forecasting with fuzzy role matching.</p>", unsafe_allow_html=True)

    left, right = st.columns([1, 1], gap="large")

    # --- LEFT PANEL -------------------------------------------------------------
    with left:
        # 1- Your Role
        st.markdown("<div class='section-label'>1 | Your Role</div>", unsafe_allow_html=True)
        job_query = st.text_input(
            label="job_role_input",
            label_visibility="collapsed",
            placeholder="e.g. AI Engineer, Data Scientist, ML Developer...",
            key="job_query"
        )

        matched_job, match_score = fuzzy_match_job(job_query, KNOWN_JOBS)

        if job_query:
            if matched_job:
                confidence = "High" if match_score >= 80 else "Good" if match_score >= 60 else "Approximate"
                st.markdown(
                    f"<div class='fuzzy-match-hint'>Matched: <strong>{matched_job}</strong> &nbsp;|&nbsp; {confidence} match ({match_score}%)</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    "<div class='fuzzy-no-match'>No close match found. Try a different title.</div>",
                    unsafe_allow_html=True
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # 2- Years of Experience
        st.markdown("<div class='section-label'>2 | Years of Experience</div>", unsafe_allow_html=True)
        exp_choice = st.radio(
            label="experience_radio",
            label_visibility="collapsed",
            options=EXPERIENCE_OPTIONS,
            index=2,
            horizontal=True,
            key="exp_radio"
        )
        experience_years = EXP_VALUE_MAP[exp_choice]

        st.markdown("<br>", unsafe_allow_html=True)

        # 3- Preferred Location
        st.markdown("<div class='section-label'>3 | Preferred Location</div>", unsafe_allow_html=True)
        loc_options = sorted(list(le_location.classes_))
        default_loc_idx = loc_options.index("Bangalore") if "Bangalore" in loc_options else 0
        location_choice = st.selectbox(
            label="location_input",
            label_visibility="collapsed",
            options=loc_options,
            index=default_loc_idx,
            key="location_input"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # 4- Core Skills
        st.markdown("<div class='section-label'>4 | Core Skills (up to 5)</div>", unsafe_allow_html=True)
        if len(st.session_state.skills) < 5:
            st.text_input(
                "Add skill",
                label_visibility="collapsed",
                placeholder=f"Type a skill and press Enter ({5 - len(st.session_state.skills)} remaining)",
                key="skill_input_val",
                on_change=submit_skill
            )
        else:
            st.markdown("<div class='skill-limit-warn'>Max 5 skills reached.</div>", unsafe_allow_html=True)

        if st.session_state.skills:
            st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
            cols = st.columns([1]*len(st.session_state.skills) + [10 - len(st.session_state.skills)])
            for i, skill in enumerate(st.session_state.skills):
                with cols[i]:
                    if st.button(f"{skill} X", key=f"del_skill_{i}", help="Click to remove"):
                        remove_skill(i)
                        st.rerun()
        else:
            st.markdown("<p style='color:#475569; font-size:0.85rem; margin:8px 0 12px'>No skills added yet.</p>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        can_predict = bool(matched_job)
        predict_btn = st.button(
            "Generate Salary Estimation",
            disabled=not can_predict,
            type="primary",
            key="predict_btn"
        )

    # --- RIGHT PANEL ------------------------------------------------------------
    with right:
        if predict_btn and matched_job:
            with st.spinner("Analysing market dynamics..."):
                skill_bonus = 1.0 + (len(st.session_state.skills) * 0.03)
                
                input_df = pd.DataFrame([{
                    "job_title_encoded": le_job.transform([matched_job])[0],
                    "location_encoded": le_location.transform([location_choice])[0],
                    "experience_years": experience_years,
                    "skill_score": compute_skill_score(st.session_state.skills)
                }])
                
                # Reorder columns to match the training feature order
                features_order = ['job_title_encoded', 'location_encoded', 'experience_years', 'skill_score']
                input_df = input_df[features_order]
                
                pred_min = max(0, min_model.predict(input_df)[0])
                pred_max = max(pred_min, max_model.predict(input_df)[0])
                
                pred_min = round(pred_min * skill_bonus, 1)
                pred_max = round(pred_max * skill_bonus, 1)

                # Freshness Guardrails
                if experience_years == 0:
                    tier_1_roles = ["Surgeon", "Investment Banker", "AI Engineer", "Pilot"]
                    fresher_max = 20.0 if any(t in matched_job for t in tier_1_roles) else 12.0
                    fresher_min = 3.5
                    pred_max = min(pred_max, fresher_max)
                    pred_min = min(pred_min, fresher_max * 0.65)
                    pred_min = max(pred_min, fresher_min)

            st.markdown(f"""
            <div class='glass-card'>
                <div class='prediction-range'>
                    <div class='pred-label'>Estimated Compensation Range</div>
                    <div class='pred-value'>Rs. {round(pred_min, 1)} - {round(pred_max, 1)} LPA</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            cc1, cc2, cc3 = st.columns(3)
            with cc1: st.metric("Matched Role", matched_job)
            with cc2: st.metric("Experience", exp_choice)
            with cc3: st.metric("Skills", f"{len(st.session_state.skills)} / 5")

            st.markdown("#### Top Employers for This Role")
            rel_data = df_raw[df_raw["job_title"] == matched_job]
            if not rel_data.empty:
                # Melt the multiple company columns into a single long-format column for the matched role
                company_base_cols = ["company_1", "company_2", "company_3", "company_4", "company_5"]
                rel_companies = pd.melt(
                    rel_data, 
                    id_vars=["salary_max_lpa"], 
                    value_vars=company_base_cols, 
                    value_name="company_name"
                )
                rel_companies = rel_companies[rel_companies["company_name"] != ""]
                
                if not rel_companies.empty:
                    top_companies = rel_companies.sort_values("salary_max_lpa", ascending=False)["company_name"].unique()[:5]
                    comp_html = ""
                    for c in top_companies:
                        comp_html += f"<span class='company-tag'>{c}</span>"
                    st.markdown(comp_html, unsafe_allow_html=True)
                else:
                    st.info("No specific company data for this role.")
            else:
                st.info("Not enough historical data for company recommendations.")

        elif not predict_btn:
            st.markdown("""
            <div class='glass-card' style='text-align:center; padding:4rem 2rem;'>
                <div style='font-size:4rem; margin-bottom:1rem'></div>
                <h3 style='color:white; margin-bottom:0.5rem'>Ready to Calculate Your Earning Potential?</h3>
                <p style='max-width: 600px; margin: 0 auto; line-height: 1.6;'>Fill in your Role, Experience, location and skills to unlock your career insights.<br>Our AI-powered engine will analyze current market trends for an accurate salary estimation.</p>
            </div>
            """, unsafe_allow_html=True)
            if job_query and not matched_job:
                st.caption("Please enter a recognisable job role to enable prediction.")

# --------------------------------------------------------
#  TAB 2 - ANALYTICS
# --------------------------------------------------------
with tab2:
    st.markdown("## Industry Market Analytics")
    st.markdown("<p>Explore salary trends, top roles, and hiring companies dynamically.</p>", unsafe_allow_html=True)

    st.subheader("Experience Bracket Filter")
    max_exp = int(df_raw["experience_years"].max())
    exp_range = st.slider("Filter by Experience (Years)", 0, max_exp, (2, 8))

    df_filtered = df_raw[
        (df_raw["experience_years"] >= exp_range[0]) & 
        (df_raw["experience_years"] <= exp_range[1])
    ]

    if df_filtered.empty:
        st.markdown(
            "<div style='padding: 1rem 1.5rem; background: rgba(99,102,241,0.1); border: 1px solid rgba(99,102,241,0.2); border-radius: 12px; color: #a5b4fc; margin-top: 1rem; text-align: center; font-weight: 500;'>No market data for this experience bracket.</div>",
            unsafe_allow_html=True
        )
    else:
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Total Roles", len(df_filtered))
        with m2: st.metric("Avg Max Salary", f"Rs. {round(df_filtered['salary_max_lpa'].mean(), 1)} LPA")
        with m3: st.metric("Top Location", df_filtered["location"].mode()[0])

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### Top Companies vs Max Salaries")
            company_base_cols = ["company_1", "company_2", "company_3", "company_4", "company_5"]
            
            # Melt the multiple company columns into a single long-format column
            df_companies = pd.melt(
                df_filtered, 
                id_vars=["salary_max_lpa"], 
                value_vars=company_base_cols, 
                value_name="company_name"
            )
            # Remove empty strings (placeholder values)
            df_companies = df_companies[df_companies["company_name"] != ""]
            
            if not df_companies.empty:
                comp_data = df_companies.groupby("company_name")["salary_max_lpa"].max().sort_values(ascending=True).tail(10).reset_index()
                fig_comp = px.bar(comp_data, x="company_name", y="salary_max_lpa", color="salary_max_lpa", color_continuous_scale="Purples", labels={"salary_max_lpa": "Max Salary (LPA)", "company_name": "Company"})
                fig_comp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=450, margin=dict(l=20, r=20, t=20, b=20))
                # Keep labels straight as requested
                fig_comp.update_xaxes(tickangle=0)
                st.plotly_chart(fig_comp, use_container_width=True)
            else:
                st.info("No company data available for this selection.")

        with c2:
            st.markdown("#### Role Demand Distribution")
            role_counts = df_filtered["job_title"].value_counts().reset_index()
            role_counts.columns = ["job_title", "count"]
            if len(role_counts) > 7:
                others_count = role_counts.iloc[7:]["count"].sum()
                role_counts = pd.concat([role_counts.head(7), pd.DataFrame([{"job_title": "Others", "count": others_count}])])
            
            fig_pie = px.pie(role_counts, values="count", names="job_title", hole=0.6, color_discrete_sequence=px.colors.sequential.Purples_r)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=450, showlegend=True, margin=dict(l=20, r=20, t=60, b=20), annotations=[dict(text=f"Total<br><b>{len(df_filtered)}</b>", x=0.5, y=0.5, font_size=20, showarrow=False)])
            st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("<div class='footer'>Advanced ML Analytics System - Powered by Random Forest + Fuzzy Logic - rapidfuzz matching enabled.</div>", unsafe_allow_html=True)
