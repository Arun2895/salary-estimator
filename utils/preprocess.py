import pandas as pd
import numpy as np

# Define company tiers for scoring
TIER_1 = [
    "google", "amazon", "microsoft", "meta", "apple", "netflix", "uber", "airbnb", "stripe",
    "slack", "github", "square", "paypal", "twitter", "linkedin", "goldman sachs", "jp morgan", 
    "morgan stanley", "citadel", "de shaw", "spacex", "tesla", "deepmind", "openai", "modifying",
    "visa", "mastercard", "blackrock", "fidelity", "moderna"
]
TIER_2 = [
    "oracle", "ibm", "intel", "nvidia", "cisco", "adobe", "salesforce", "hubspot", "snowflake",
    "servicenow", "palantir", "publicis", "wpp", "dentsu", "omnicom", "pfizer", "novartis", 
    "roche", "merck", "glaxosmithkline", "astrazeneca", "bayer", "abbott", "lockheed martin", 
    "northrop grumman", "boeing"
]
TIER_3 = [
    "tcs", "infosys", "wipro", "hcl tech", "cognizant", "capgemini", "accenture", "tech mahindra",
    "icici bank", "hdfc bank", "hsbc", "standard chartered", "deloitte", "pwc", "ey", "kpmg",
    "apollo hospitals", "practo", "biocon", "tata", "mahindra", "reliance"
]

def load_data(path):
    return pd.read_csv(path)

def clean_data(df):
    df = df.dropna()
    for i in range(1, 6):
        col = f"company_{i}"
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower()
    return df

def encode_location(location):
    location = str(location).lower()
    if "bangalore" in location or "delhi" in location:
        return 3
    elif "pune" in location or "chennai" in location:
        return 2
    else:
        return 1

def encode_industry(industry):
    industry = str(industry).lower()
    mapping = {
        "healthcare": 3,
        "finance": 3,
        "marketing": 2,
        "science": 3,
        "it": 3,
        "accounting": 2
    }
    return mapping.get(industry, 2)

def get_company_tier_score(name):
    name = str(name).lower().strip()
    if not name or name in ["nan", "none"]: return 1
    if any(t in name for t in TIER_1): return 4
    if any(t in name for t in TIER_2): return 3
    if any(t in name for t in TIER_3): return 2
    return 1

def compute_company_score(row):
    comp_names = [
        row.get("company_1", ""),
        row.get("company_2", ""),
        row.get("company_3", ""),
        row.get("company_4", ""),
        row.get("company_5", "")
    ]
    
    scores = []
    for name in comp_names:
        name = str(name).lower().strip()
        if name and name not in ["nan", "none", ""]:
            scores.append(get_company_tier_score(name))
            
    if not scores:
        return 1.0
        
    return sum(scores) / len(scores)

# -------------------------
# SKILL SCORING SYSTEM
# -------------------------

SKILL_IMPORTANCE = {
    "python": 10, "sql": 9, "sas": 9, "r": 8, "data analysis": 8,
    "risk management": 9, "epidemiology": 8, "biostatistics": 8,
    "seo": 6, "vba": 6, "machine learning": 10, "deep learning": 10,
    "aws": 9, "docker": 9, "kubernetes": 9, "react": 8, "nodejs": 8,
    "javascript": 7, "java": 10, "cpp": 9, "c++": 9, "bash": 7, "linux": 7,
    "terraform": 7, "jenkins": 8, "ci/cd": 8,
    # Data Analyst / Engineer
    "airflow": 9, "etl": 9, "spark": 9, "hadoop": 8, "power bi": 8, "powerbi": 8,
    "dbt": 9, "snowflake": 9, "kafka": 9, "big data": 8, "matplotlib": 7, "pandas": 8,
    # Academic & Teaching
    "pedagogy": 7, "curriculum design": 8, "teaching": 7, "mentoring": 7,
    "research": 9, "public speaking": 8, "academic writing": 8, "grant writing": 8,
    "student assessment": 7, "subject expertise": 7, "instructional design": 8, "lms": 7,
    # HR & Operations
    "recruiting": 8, "talent acquisition": 8, "employee relations": 7,
    "onboarding": 7, "payroll": 7, "hris": 8, "project management": 9, "agile": 8, "scrum": 8,
    "performance management": 8, "l&d": 7, "jd writing": 6, "ats": 7,
    # Design & Creative
    "photoshop": 8, "illustrator": 8, "figma": 9, "ui/ux": 9, "ui design": 8, "ux design": 9,
    "typography": 7, "indesign": 7, "branding": 8, "editing": 7, "photography": 7,
    "after effects": 8, "premiere pro": 8, "motion graphics": 8, "color grading": 7,
    "design systems": 9, "usability testing": 8, "product thinking": 9, "sketch": 7,
    "cinema 4d": 8, "animation": 8, "wireframing": 8, "prototyping": 8,
    # Engineering
    "autocad": 8, "solidworks": 9, "thermodynamics": 8, "manufacturing": 8,
    "matlab": 8, "ansys": 8, "plc": 8, "embedded systems": 9, "scada": 8,
    "aerodynamics": 8, "fluid dynamics": 8, "control systems": 9, "ros": 9,
    "cad/cam": 8, "staad pro": 8, "aspen plus": 8, "kinematics": 8,
    # Business & Sales
    "sales": 8, "crm": 7, "b2b": 8, "lead generation": 7, "negotiation": 8,
    "salesforce": 8, "forecasting": 7, "market research": 7, "cold calling": 6,
    "partnership development": 7, "property valuation": 8, "real estate": 7,
    # Medical & Healthcare
    "patient care": 8, "diagnosis": 9, "surgery": 10, "emr": 7, "anatomy": 8,
    "medical research": 9, "bls": 7, "cpr": 7, "psychotherapy": 8, "cbt": 8,
    "dentistry": 9, "oral surgery": 9, "pharmacology": 8, "clinical skills": 8,
    "physiotherapy": 8, "rehabilitation": 7, "radiology": 9, "mri interpretation": 9,
    "clinical research": 9, "regulatory affairs": 8, "drug discovery": 9,
    "prosthodontics": 8, "orthodontics": 8, "counseling": 7, "mental health": 8,
    "laparoscopic surgery": 10, "emergency medicine": 9, "evidence-based medicine": 8,
    "medication administration": 7, "icu care": 8, "vital signs": 6,
    # Trades & Construction
    "wiring": 8, "troubleshooting": 7, "electrical systems": 8, "safety": 7,
    "blueprint reading": 8, "piping": 8, "welding": 8, "fabrication": 8,
    "woodworking": 7, "framing": 7, "power tools": 6, "hvac systems": 8,
    "refrigeration": 7, "metalworking": 7, "hydraulics": 7, "tig/mig welding": 8,
    # Legal
    "litigation": 9, "legal writing": 8, "corporate law": 9, "contract negotiation": 9,
    "compliance": 8, "case management": 7, "lexisnexis": 8, "m&a": 9,
    "intellectual property": 8, "gdpr": 8, "kyc/aml": 8, "legal analysis": 8,
    "legal research": 8, "court filing": 7, "document drafting": 7,
    # Niche IT
    "solidity": 9, "smart contracts": 9, "cryptography": 9, "web3": 8,
    "unity": 8, "unreal engine": 9, "c#": 8, "database design": 9,
    "performance tuning": 9, "penetration testing": 10, "burp suite": 8, "metasploit": 8,
    "swift": 9, "kotlin": 8, "android sdk": 8, "swiftui": 8, "jetpack compose": 9,
    "graphql": 8, "typescript": 8, "redis": 8, "postgresql": 8, "mongodb": 8,
    "kali linux": 8, "siem": 8, "soc": 8, "vulnerability assessment": 9, "firewalls": 7,
    "backup & recovery": 7, "pl/sql": 8, "oracle": 8, "mysql": 8,
    "defi": 9, "opengl": 8, "directx": 8, "3d math": 8, "game design": 8,
    "rust": 9, "ethereum": 8, "room db": 7, "firebase": 7, "testflight": 6, "xcode": 7,
    # Finance
    "financial modeling": 9, "valuation": 9, "dcf analysis": 9, "derivatives": 9,
    "actuarial science": 9, "probability": 8, "credit risk": 8, "portfolio management": 9,
    "wealth management": 9, "auditing": 7, "taxation": 7, "ifrs": 8, "gst": 7,
    "stochastic calculus": 9, "credit analysis": 8, "bloomberg": 8,
    "income tax": 7, "tally": 6, "internal controls": 7, "financial planning": 8,
    # Science
    "genomics": 9, "ngs": 9, "bioinformatics tools": 8, "spectroscopy": 8, "gmp": 7,
    "quantum mechanics": 9, "experiment design": 8, "lab techniques": 7,
    "chromatography": 7, "statistical modeling": 9,
    # Marketing
    "sem": 7, "social media": 6, "email marketing": 6, "content strategy": 7,
    "copywriting": 6, "a/b testing": 8, "consumer insights": 7,
    "campaign management": 7, "budget management": 7, "content writing": 6,
    # Operations
    "supply chain": 8, "logistics": 7, "procurement": 7, "sap": 8, "erp": 8,
    "six sigma": 8, "vendor management": 7, "product management": 9,
    "roadmap planning": 8, "stakeholder management": 8, "inventory management": 7,
    "ms project": 7, "pmp": 8, "jira": 7,
    # Entertainment
    "acting": 8, "improvisation": 7, "voice acting": 7, "script analysis": 7,
    "directing": 9, "screenwriting": 9, "cinematography": 8, "music theory": 7,
    "composing": 8, "live performance": 7, "arrangement": 7, "davinci resolve": 8,
    # Data Science extras
    "statistics": 9, "scikit-learn": 8, "tensorflow": 9, "pytorch": 10,
    "nlp": 9, "computer vision": 9, "mlops": 9, "mlflow": 8, "transformers": 10,
    "feature engineering": 8, "looker": 8, "bigquery": 9, "data warehouse": 9,
    "data modeling": 9, "analytics": 8, "azure": 9, "gcp": 9, "ansible": 8,
    "microservices": 9, "rest api": 8, "system design": 9, "distributed systems": 10,
    "architecture": 9, "algorithms": 9, "data structures": 9, "git": 6,
    "monitoring": 7, "incident management": 8, "slo/sla": 7, "networking": 7,
    "requirements gathering": 7, "leadership": 9, "administration": 7
}

def compute_skill_score(input_data):
    """
    Computes a weighted skill score from 0-1.
    Handles both a row (dict/Series with skill_1..5) or a list of skills.
    """
    if isinstance(input_data, list):
        raw_skills = [str(s) for s in input_data]
    elif hasattr(input_data, "get"):
        raw_skills = [
            str(input_data.get("skill_1", "")),
            str(input_data.get("skill_2", "")),
            str(input_data.get("skill_3", "")),
            str(input_data.get("skill_4", "")),
            str(input_data.get("skill_5", ""))
        ]
    else:
        # Fallback for unexpected types
        raw_skills = [str(input_data)]
    
    # In case skills are comma separated in one column
    all_skills = []
    for s in raw_skills:
        if s.lower() not in ["nan", "none", ""]:
            # Handle potential comma-separated values if the string contains them
            all_skills.extend([x.strip() for x in s.split(",")])
            
    filtered_skills = [s.lower() for s in all_skills if s and s != "nan"]

    if not filtered_skills:
        return 4.0
    
    scores = []
    for skill in filtered_skills:
        score = 6
        for key, val in SKILL_IMPORTANCE.items():
            if key in skill:
                score = max(score, val)
        scores.append(score)

    # Sum the scores so that more skills explicitly yield a higher overall score
    return float(sum(scores))

def preprocess_dataframe(df):
    """
    Prepared the full dataframe for model training.
    """
    df = clean_data(df)
    
    # Features
    df["skill_score"] = df.apply(compute_skill_score, axis=1)
    df["industry_score"] = df["industry"].apply(encode_industry)
    df["location_score"] = df["location"].apply(encode_location)
    df["company_score"] = df.apply(compute_company_score, axis=1)
    
    return df