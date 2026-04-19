import pandas as pd
import numpy as np
import random
import os

random.seed(42)
np.random.seed(42)

# ─────────────────────────────────────────────────────────────────────────────
#  ROLE PROFILES  (all salaries are in Indian LPA — 2024/2026 market data)
#
#  sal_p0  : realistic fresher/0-yr salary (LPA)
#  sal_p5  : realistic 5-yr salary (LPA)
#  sal_p10 : realistic 10-yr salary (LPA)
#  sal_p20 : realistic 20-yr peak salary (LPA)
#
#  Sources: AmbitionBox, Naukri, LinkedIn, Glassdoor (India), industry reports
#  Data reflects MEDIAN market, not outliers like top-tier FAANG packages
# ─────────────────────────────────────────────────────────────────────────────
PROFILES = {

    # ── Software / Tech ───────────────────────────────────────────────────────
    "Software Engineer":         {"sal_p0":  5,  "sal_p5": 18, "sal_p10": 35, "sal_p20": 55, "industry": "IT",
                                  "skills": ["Python", "Java", "C++", "Data Structures", "Algorithms", "Git", "SQL", "System Design", "Linux", "Agile"]},
    "Senior Software Engineer":  {"sal_p0": 18,  "sal_p5": 28, "sal_p10": 45, "sal_p20": 70, "industry": "IT",
                                  "skills": ["Python", "Java", "System Design", "Microservices", "AWS", "Docker", "Leadership", "Mentoring", "CI/CD", "Algorithms"]},
    "Staff Engineer":            {"sal_p0": 35,  "sal_p5": 50, "sal_p10": 70, "sal_p20": 100, "industry": "IT",
                                  "skills": ["System Design", "Architecture", "Leadership", "Python", "Java", "Distributed Systems", "Mentoring", "AWS"]},
    "AI Engineer":               {"sal_p0": 10,  "sal_p5": 25, "sal_p10": 50, "sal_p20": 90, "industry": "IT",
                                  "skills": ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "NLP", "Computer Vision", "CUDA", "MLOps", "Transformers"]},
    "ML Engineer":               {"sal_p0":  9,  "sal_p5": 22, "sal_p10": 40, "sal_p20": 75, "industry": "IT",
                                  "skills": ["Python", "Machine Learning", "AWS", "Docker", "Kubernetes", "C++", "Spark", "MLflow", "Feature Engineering", "Scikit-Learn"]},
    "Data Scientist":            {"sal_p0":  7,  "sal_p5": 20, "sal_p10": 38, "sal_p20": 65, "industry": "IT",
                                  "skills": ["Python", "R", "Machine Learning", "Data Analysis", "SQL", "Pandas", "Statistics", "Tableau", "A/B Testing", "Scikit-Learn"]},
    "Data Analyst":              {"sal_p0":  4,  "sal_p5": 10, "sal_p10": 18, "sal_p20": 28, "industry": "IT",
                                  "skills": ["SQL", "Excel", "Tableau", "Power BI", "Python", "Data Analysis", "Pandas", "Google Analytics", "Looker", "Statistics"]},
    "Data Engineer":             {"sal_p0":  7,  "sal_p5": 18, "sal_p10": 32, "sal_p20": 55, "industry": "IT",
                                  "skills": ["Python", "SQL", "Spark", "Hadoop", "ETL", "Airflow", "Snowflake", "Kafka", "DBT", "Data Warehouse", "BigQuery", "AWS"]},
    "Business Analyst":          {"sal_p0":  5,  "sal_p5": 12, "sal_p10": 20, "sal_p20": 32, "industry": "IT",
                                  "skills": ["SQL", "Excel", "Tableau", "Requirements Gathering", "Stakeholder Management", "Agile", "JIRA", "Data Analysis", "Power BI"]},
    "Backend Developer":         {"sal_p0":  6,  "sal_p5": 16, "sal_p10": 30, "sal_p20": 50, "industry": "IT",
                                  "skills": ["Java", "Python", "NodeJS", "SQL", "AWS", "Docker", "REST API", "Microservices", "Redis", "PostgreSQL"]},
    "Frontend Developer":        {"sal_p0":  5,  "sal_p5": 14, "sal_p10": 25, "sal_p20": 42, "industry": "IT",
                                  "skills": ["React", "JavaScript", "TypeScript", "HTML/CSS", "Vue", "Angular", "Redux", "UI/UX", "Webpack", "GraphQL"]},
    "Full Stack Developer":      {"sal_p0":  6,  "sal_p5": 16, "sal_p10": 28, "sal_p20": 48, "industry": "IT",
                                  "skills": ["React", "NodeJS", "Python", "SQL", "AWS", "Docker", "TypeScript", "REST API", "MongoDB", "Redis"]},
    "Cloud Engineer":            {"sal_p0":  7,  "sal_p5": 18, "sal_p10": 32, "sal_p20": 55, "industry": "IT",
                                  "skills": ["AWS", "Azure", "GCP", "Terraform", "Kubernetes", "Linux", "Networking", "Docker", "CI/CD", "Security"]},
    "DevOps Engineer":           {"sal_p0":  7,  "sal_p5": 18, "sal_p10": 30, "sal_p20": 52, "industry": "IT",
                                  "skills": ["Jenkins", "CI/CD", "AWS", "Docker", "Kubernetes", "Bash", "Terraform", "Ansible", "Monitoring", "Linux"]},
    "Site Reliability Engineer": {"sal_p0":  8,  "sal_p5": 20, "sal_p10": 35, "sal_p20": 58, "industry": "IT",
                                  "skills": ["Linux", "Python", "Kubernetes", "AWS", "Monitoring", "Incident Management", "SLO/SLA", "Docker", "Automation", "Networking"]},
    "Cybersecurity Analyst":     {"sal_p0":  6,  "sal_p5": 15, "sal_p10": 28, "sal_p20": 50, "industry": "IT",
                                  "skills": ["Network Security", "Penetration Testing", "Python", "Linux", "Firewalls", "SIEM", "SOC", "Vulnerability Assessment", "Cryptography"]},
    "Ethical Hacker":            {"sal_p0":  7,  "sal_p5": 16, "sal_p10": 28, "sal_p20": 50, "industry": "IT",
                                  "skills": ["Penetration Testing", "Network Security", "Cryptography", "Linux", "Python", "Burp Suite", "Metasploit", "Kali Linux"]},
    "Blockchain Developer":      {"sal_p0":  8,  "sal_p5": 20, "sal_p10": 35, "sal_p20": 60, "industry": "IT",
                                  "skills": ["Solidity", "Smart Contracts", "Cryptography", "Ethereum", "Web3", "Rust", "DeFi", "JavaScript"]},
    "Game Developer":            {"sal_p0":  4,  "sal_p5": 12, "sal_p10": 22, "sal_p20": 40, "industry": "IT",
                                  "skills": ["Unity", "C#", "Unreal Engine", "C++", "3D Math", "Game Design", "OpenGL", "DirectX"]},
    "Database Administrator":    {"sal_p0":  5,  "sal_p5": 12, "sal_p10": 22, "sal_p20": 38, "industry": "IT",
                                  "skills": ["SQL", "Oracle", "MySQL", "PostgreSQL", "Database Design", "Performance Tuning", "Backup & Recovery", "PL/SQL"]},
    "Android Developer":         {"sal_p0":  5,  "sal_p5": 14, "sal_p10": 25, "sal_p20": 42, "industry": "IT",
                                  "skills": ["Kotlin", "Java", "Android SDK", "REST API", "Firebase", "Git", "Jetpack Compose", "Room DB"]},
    "iOS Developer":             {"sal_p0":  6,  "sal_p5": 15, "sal_p10": 26, "sal_p20": 45, "industry": "IT",
                                  "skills": ["Swift", "Objective-C", "Xcode", "CoreData", "SwiftUI", "REST API", "Firebase", "TestFlight"]},
    "Analytics Engineer":        {"sal_p0":  7,  "sal_p5": 18, "sal_p10": 30, "sal_p20": 50, "industry": "IT",
                                  "skills": ["DBT", "SQL", "Snowflake", "Python", "Data Warehouse", "Airflow", "Analytics", "Data Modeling"]},
    "Research Analyst":          {"sal_p0":  4,  "sal_p5":  9, "sal_p10": 15, "sal_p20": 25, "industry": "IT",
                                  "skills": ["Data Analysis", "Excel", "Research", "SQL", "Python", "Report Writing", "Statistics"]},

    # ── Healthcare / Medical ─────────────────────────────────────────────────
    # MBBS fresher in govt: ~7 LPA, private: 5–10 LPA
    "Doctor":                    {"sal_p0":  7,  "sal_p5": 15, "sal_p10": 28, "sal_p20": 50, "industry": "Healthcare",
                                  "skills": ["Patient Care", "Diagnosis", "Clinical Skills", "Medical Research", "EMR", "Anatomy", "Emergency Medicine", "Evidence-Based Medicine"]},
    # Surgeon needs 5+ yrs post MBBS before independent practice
    "Surgeon":                   {"sal_p0": 12,  "sal_p5": 30, "sal_p10": 55, "sal_p20": 90, "industry": "Healthcare",
                                  "skills": ["Surgery", "Patient Care", "Anatomy", "Diagnosis", "Emergency Medicine", "Laparoscopic Surgery"]},
    # BDS fresher: 3–5 LPA; private practice later booms
    "Dentist":                   {"sal_p0":  4,  "sal_p5":  9, "sal_p10": 18, "sal_p20": 35, "industry": "Healthcare",
                                  "skills": ["Dentistry", "Oral Surgery", "Patient Care", "Diagnosis", "Prosthodontics", "Orthodontics"]},
    # Staff Nurse: BSc Nursing 2.5–4 LPA fresher
    "Nurse":                     {"sal_p0":  3,  "sal_p5":  5, "sal_p10":  9, "sal_p20": 14, "industry": "Healthcare",
                                  "skills": ["Patient Care", "BLS", "CPR", "EMR", "Vital Signs", "Medication Administration", "ICU Care"]},
    "Physiotherapist":           {"sal_p0":  3,  "sal_p5":  6, "sal_p10": 10, "sal_p20": 18, "industry": "Healthcare",
                                  "skills": ["Physiotherapy", "Rehabilitation", "Manual Therapy", "Patient Care", "Exercise Therapy"]},
    "Psychologist":              {"sal_p0":  3,  "sal_p5":  7, "sal_p10": 12, "sal_p20": 22, "industry": "Healthcare",
                                  "skills": ["Psychotherapy", "CBT", "Mental Health", "Counseling", "Assessment", "Patient Care"]},
    # B.Pharm fresher: 2.5–4 LPA
    "Pharmacist":                {"sal_p0":  3,  "sal_p5":  5, "sal_p10":  9, "sal_p20": 15, "industry": "Healthcare",
                                  "skills": ["Pharmacology", "Patient Counseling", "Drug Interactions", "Compounding", "Inventory Management"]},
    # Radiologist needs MD Radiodiagnosis — PG finished = 5–8 yrs after MBBS
    "Radiologist":               {"sal_p0": 12,  "sal_p5": 25, "sal_p10": 45, "sal_p20": 75, "industry": "Healthcare",
                                  "skills": ["Radiology", "MRI Interpretation", "CT Scan", "X-Ray", "Patient Care", "Diagnosis"]},
    "Biostatistician":           {"sal_p0":  5,  "sal_p5": 11, "sal_p10": 20, "sal_p20": 35, "industry": "Healthcare",
                                  "skills": ["R", "SAS", "Biostatistics", "Epidemiology", "Clinical Trials", "SPSS", "Python"]},
    "Pharmacologist":            {"sal_p0":  5,  "sal_p5": 12, "sal_p10": 22, "sal_p20": 38, "industry": "Healthcare",
                                  "skills": ["Pharmacology", "Research", "Chemistry", "Data Analysis", "Regulatory Affairs", "Clinical Research"]},

    # ── Education / Academia ─────────────────────────────────────────────────
    # UGC scale 7th CPC: Asst Prof 7-CPC Level 10 = ~7 LPA
    "Professor":                 {"sal_p0":  9,  "sal_p5": 14, "sal_p10": 22, "sal_p20": 35, "industry": "Education",
                                  "skills": ["Teaching", "Research", "Curriculum Design", "Mentoring", "Public Speaking", "Academic Writing", "Pedagogy", "Grant Writing"]},
    "Associate Professor":       {"sal_p0":  7,  "sal_p5": 12, "sal_p10": 18, "sal_p20": 28, "industry": "Education",
                                  "skills": ["Teaching", "Research", "Mentoring", "Academic Writing", "Curriculum Design", "Pedagogy"]},
    # UGC Level 10 starting: ~6.5–8 LPA
    "Assistant Professor":       {"sal_p0":  6,  "sal_p5": 10, "sal_p10": 15, "sal_p20": 22, "industry": "Education",
                                  "skills": ["Teaching", "Research", "Mentoring", "Academic Writing", "Pedagogy", "Subject Expertise"]},
    # Private school: 2.5–4 LPA; govt 4–7 LPA
    "Teacher":                   {"sal_p0":  3,  "sal_p5":  5, "sal_p10":  8, "sal_p20": 14, "industry": "Education",
                                  "skills": ["Teaching", "Pedagogy", "Curriculum Design", "Mentoring", "Classroom Management", "Student Assessment"]},
    "Lecturer":                  {"sal_p0":  3,  "sal_p5":  6, "sal_p10": 10, "sal_p20": 16, "industry": "Education",
                                  "skills": ["Teaching", "Pedagogy", "Public Speaking", "Academic Writing", "Subject Expertise", "Curriculum Design"]},
    "School Principal":          {"sal_p0":  5,  "sal_p5":  9, "sal_p10": 14, "sal_p20": 22, "industry": "Education",
                                  "skills": ["Leadership", "Administration", "Curriculum Design", "Stakeholder Management", "Budget Management", "HR"]},
    "Education Consultant":      {"sal_p0":  4,  "sal_p5":  9, "sal_p10": 15, "sal_p20": 25, "industry": "Education",
                                  "skills": ["Curriculum Design", "Training", "E-Learning", "Instructional Design", "LMS", "Project Management"]},

    # ── Finance / Accounting ─────────────────────────────────────────────────
    # CA fresher: Big 4 6–9 LPA; avg 5–7 LPA
    "Financial Analyst":         {"sal_p0":  5,  "sal_p5": 12, "sal_p10": 22, "sal_p20": 38, "industry": "Finance",
                                  "skills": ["Excel", "Financial Modeling", "VBA", "Accounting", "Data Analysis", "Bloomberg", "Valuation", "SQL"]},
    # IB fresher (Tier-1 firm): 12–18 LPA; avg firm 8–12
    "Investment Banker":         {"sal_p0": 10,  "sal_p5": 25, "sal_p10": 50, "sal_p20": 90, "industry": "Finance",
                                  "skills": ["Financial Modeling", "Valuation", "Excel", "Negotiation", "Accounting", "DCF Analysis", "Pitch Books", "M&A"]},
    # Actuary (early exam passes get premium)
    "Actuary":                   {"sal_p0":  8,  "sal_p5": 18, "sal_p10": 32, "sal_p20": 55, "industry": "Finance",
                                  "skills": ["Actuarial Science", "Statistics", "R", "Excel", "Risk Management", "SAS", "Python", "Probability"]},
    # Quant — IIT/IIM + good math = high fresher
    "Quant Analyst":             {"sal_p0": 10,  "sal_p5": 28, "sal_p10": 55, "sal_p20": 95, "industry": "Finance",
                                  "skills": ["Python", "C++", "Mathematics", "Machine Learning", "Statistics", "R", "Stochastic Calculus", "Derivatives"]},
    "Risk Analyst":              {"sal_p0":  5,  "sal_p5": 12, "sal_p10": 22, "sal_p20": 38, "industry": "Finance",
                                  "skills": ["Risk Management", "SQL", "Excel", "Python", "Data Analysis", "Compliance", "Basel", "Credit Risk"]},
    # GST/Tax consultant at Big 4: 5–8 LPA fresher
    "Tax Consultant":            {"sal_p0":  5,  "sal_p5": 10, "sal_p10": 18, "sal_p20": 30, "industry": "Finance",
                                  "skills": ["Taxation", "Accounting", "Auditing", "Excel", "Compliance", "GST", "Income Tax", "Tally"]},
    # CA: Big 4 salary 6–9 LPA, PSU 7–10 LPA
    "Chartered Accountant":      {"sal_p0":  7,  "sal_p5": 14, "sal_p10": 25, "sal_p20": 42, "industry": "Finance",
                                  "skills": ["Accounting", "Auditing", "Taxation", "Excel", "Financial Reporting", "Compliance", "IFRS", "SAP"]},
    "Auditor":                   {"sal_p0":  4,  "sal_p5":  9, "sal_p10": 16, "sal_p20": 28, "industry": "Finance",
                                  "skills": ["Auditing", "Accounting", "Compliance", "Excel", "Risk Management", "Internal Controls"]},
    "Wealth Manager":            {"sal_p0":  6,  "sal_p5": 15, "sal_p10": 28, "sal_p20": 50, "industry": "Finance",
                                  "skills": ["Wealth Management", "Portfolio Management", "Financial Planning", "Sales", "Investments", "Client Relations", "Excel"]},
    "Credit Analyst":            {"sal_p0":  5,  "sal_p5": 11, "sal_p10": 20, "sal_p20": 35, "industry": "Finance",
                                  "skills": ["Credit Analysis", "Financial Modeling", "Excel", "SQL", "Accounting", "Risk Management"]},

    # ── Core Engineering ─────────────────────────────────────────────────────
    # Mech/Civil are lower-paid in India; L&T freshers ~3.5–5 LPA
    "Mechanical Engineer":       {"sal_p0":  4,  "sal_p5":  9, "sal_p10": 16, "sal_p20": 28, "industry": "Engineering",
                                  "skills": ["AutoCAD", "SolidWorks", "Thermodynamics", "Manufacturing", "Matlab", "Ansys", "CAD/CAM", "Product Design"]},
    "Civil Engineer":            {"sal_p0":  3,  "sal_p5":  7, "sal_p10": 12, "sal_p20": 22, "industry": "Engineering",
                                  "skills": ["AutoCAD", "Project Management", "Structural Analysis", "Construction Management", "Surveying", "STAAD Pro", "Estimation"]},
    "Electrical Engineer":       {"sal_p0":  4,  "sal_p5":  9, "sal_p10": 16, "sal_p20": 28, "industry": "Engineering",
                                  "skills": ["Circuit Design", "Matlab", "AutoCAD", "Power Systems", "PLC", "C++", "Embedded Systems", "SCADA"]},
    "Chemical Engineer":         {"sal_p0":  4,  "sal_p5": 10, "sal_p10": 18, "sal_p20": 30, "industry": "Engineering",
                                  "skills": ["Chemical Process Design", "Thermodynamics", "Matlab", "Safety", "Aspen Plus", "Process Simulation"]},
    "Aerospace Engineer":        {"sal_p0":  5,  "sal_p5": 12, "sal_p10": 22, "sal_p20": 38, "industry": "Engineering",
                                  "skills": ["Aerodynamics", "Matlab", "Ansys", "CAD", "Fluid Dynamics", "C++", "Control Systems"]},
    "Robotics Engineer":         {"sal_p0":  7,  "sal_p5": 18, "sal_p10": 32, "sal_p20": 55, "industry": "Engineering",
                                  "skills": ["ROS", "C++", "Python", "Machine Learning", "Kinematics", "Computer Vision", "Embedded Systems", "Control Systems"]},

    # ── Legal ────────────────────────────────────────────────────────────────
    # Freshers at tier-1 law firms: 5–8 LPA; avg bar: 3–5 LPA
    "Lawyer":                    {"sal_p0":  4,  "sal_p5": 12, "sal_p10": 25, "sal_p20": 50, "industry": "Legal",
                                  "skills": ["Litigation", "Legal Writing", "Research", "Negotiation", "Corporate Law", "Contract Drafting", "Legal Analysis"]},
    "Corporate Counsel":         {"sal_p0": 10,  "sal_p5": 22, "sal_p10": 40, "sal_p20": 70, "industry": "Legal",
                                  "skills": ["Corporate Law", "Contract Negotiation", "Compliance", "M&A", "Risk Management", "Intellectual Property"]},
    "Paralegal":                 {"sal_p0":  3,  "sal_p5":  6, "sal_p10": 10, "sal_p20": 18, "industry": "Legal",
                                  "skills": ["Legal Research", "Document Drafting", "Case Management", "LexisNexis", "Court Filing", "Client Communication"]},
    "Compliance Officer":        {"sal_p0":  6,  "sal_p5": 13, "sal_p10": 24, "sal_p20": 40, "industry": "Legal",
                                  "skills": ["Compliance", "Risk Management", "Regulatory Affairs", "Audit", "Legal Knowledge", "GDPR", "KYC/AML"]},

    # ── Design / Creative ────────────────────────────────────────────────────
    # UX at product companies: 6–10 LPA fresher
    "UX Designer":               {"sal_p0":  5,  "sal_p5": 14, "sal_p10": 25, "sal_p20": 42, "industry": "Design",
                                  "skills": ["Figma", "UI/UX", "User Research", "Wireframing", "Prototyping", "Interaction Design", "Design Systems", "Usability Testing"]},
    "Graphic Designer":          {"sal_p0":  3,  "sal_p5":  7, "sal_p10": 12, "sal_p20": 20, "industry": "Design",
                                  "skills": ["Photoshop", "Illustrator", "InDesign", "Typography", "Branding", "Color Theory", "Print Design"]},
    # Product Designer is more senior than UX
    "Product Designer":          {"sal_p0":  6,  "sal_p5": 16, "sal_p10": 28, "sal_p20": 48, "industry": "Design",
                                  "skills": ["Figma", "UI/UX", "Product Thinking", "Design Systems", "Prototyping", "User Research", "Sketch"]},
    "Motion Designer":           {"sal_p0":  3,  "sal_p5":  8, "sal_p10": 14, "sal_p20": 24, "industry": "Design",
                                  "skills": ["After Effects", "Premiere Pro", "Motion Graphics", "Illustrator", "Cinema 4D", "Animation"]},

    # ── HR & Operations ──────────────────────────────────────────────────────
    # HR exec fresher: 3–5 LPA; HR Manager (with 5 yrs): 8–14 LPA
    "HR Manager":                {"sal_p0":  4,  "sal_p5": 10, "sal_p10": 18, "sal_p20": 30, "industry": "Operations",
                                  "skills": ["Recruiting", "Employee Relations", "Onboarding", "HRIS", "Talent Acquisition", "Payroll", "L&D", "Performance Management"]},
    "Talent Acquisition Specialist": {"sal_p0":  4,  "sal_p5":  8, "sal_p10": 14, "sal_p20": 22, "industry": "Operations",
                                  "skills": ["Recruiting", "Talent Acquisition", "LinkedIn Recruiting", "ATS", "Interview Skills", "Headhunting", "JD Writing"]},
    "Operations Manager":        {"sal_p0":  5,  "sal_p5": 13, "sal_p10": 22, "sal_p20": 38, "industry": "Operations",
                                  "skills": ["Project Management", "Agile", "Logistics", "Process Improvement", "Supply Chain", "CRM", "Six Sigma", "ERP"]},
    "Supply Chain Manager":      {"sal_p0":  5,  "sal_p5": 12, "sal_p10": 20, "sal_p20": 35, "industry": "Operations",
                                  "skills": ["Supply Chain", "Logistics", "Procurement", "ERP", "SAP", "Inventory Management", "Vendor Management"]},
    # PM in product companies: highly paid; avg 10–14 LPA fresher (MBA/eng)
    "Product Manager":           {"sal_p0":  9,  "sal_p5": 22, "sal_p10": 40, "sal_p20": 65, "industry": "Operations",
                                  "skills": ["Product Management", "Agile", "Roadmap Planning", "Stakeholder Management", "SQL", "UX Understanding", "Data Analysis", "JIRA"]},
    "Project Manager":           {"sal_p0":  6,  "sal_p5": 14, "sal_p10": 24, "sal_p20": 40, "industry": "Operations",
                                  "skills": ["Project Management", "Agile", "Scrum", "PMP", "Stakeholder Management", "Risk Management", "JIRA", "MS Project"]},
    "Business Development Manager": {"sal_p0":  5,  "sal_p5": 14, "sal_p10": 25, "sal_p20": 45, "industry": "Operations",
                                  "skills": ["Sales", "Negotiation", "B2B", "CRM", "Lead Generation", "Market Research", "Partnership Development"]},

    # ── Marketing ────────────────────────────────────────────────────────────
    "Digital Marketing Manager": {"sal_p0":  4,  "sal_p5": 10, "sal_p10": 18, "sal_p20": 30, "industry": "Marketing",
                                  "skills": ["SEO", "SEM", "Google Analytics", "Social Media", "Email Marketing", "Content Strategy", "Google Ads", "A/B Testing"]},
    "Content Strategist":        {"sal_p0":  3,  "sal_p5":  8, "sal_p10": 14, "sal_p20": 22, "industry": "Marketing",
                                  "skills": ["Content Writing", "SEO", "Content Strategy", "Social Media", "Copywriting", "Analytics"]},
    "Brand Manager":             {"sal_p0":  6,  "sal_p5": 14, "sal_p10": 24, "sal_p20": 40, "industry": "Marketing",
                                  "skills": ["Branding", "Marketing Strategy", "Market Research", "Campaign Management", "Budget Management", "Consumer Insights"]},
    "Marketing Analyst":         {"sal_p0":  4,  "sal_p5":  9, "sal_p10": 16, "sal_p20": 26, "industry": "Marketing",
                                  "skills": ["Google Analytics", "SEO", "Data Analysis", "Excel", "SQL", "Tableau", "Market Research", "A/B Testing"]},

    # ── Entertainment / Creative ─────────────────────────────────────────────
    # These are highly variable; range can be wide
    "Actor":                     {"sal_p0":  2,  "sal_p5":  8, "sal_p10": 25, "sal_p20": 80, "industry": "Entertainment",
                                  "skills": ["Acting", "Improvisation", "Voice Acting", "Public Speaking", "Script Analysis", "Physical Acting"]},
    "Film Director":             {"sal_p0":  4,  "sal_p5": 15, "sal_p10": 40, "sal_p20": 120, "industry": "Entertainment",
                                  "skills": ["Directing", "Video Production", "Screenwriting", "Leadership", "Editing", "Cinematography", "Storytelling"]},
    "Musician":                  {"sal_p0":  2,  "sal_p5":  5, "sal_p10": 15, "sal_p20": 45, "industry": "Entertainment",
                                  "skills": ["Music Theory", "Instrumental", "Composing", "Audio Editing", "Live Performance", "Arrangement"]},
    "Video Editor":              {"sal_p0":  3,  "sal_p5":  8, "sal_p10": 14, "sal_p20": 24, "industry": "Entertainment",
                                  "skills": ["Premiere Pro", "After Effects", "Color Grading", "Audio Editing", "Storytelling", "DaVinci Resolve"]},
    "Photographer":              {"sal_p0":  2,  "sal_p5":  6, "sal_p10": 12, "sal_p20": 22, "industry": "Entertainment",
                                  "skills": ["Photography", "Lightroom", "Photoshop", "Lighting", "Composition", "Retouching"]},

    # ── Trades & Skilled Labor ────────────────────────────────────────────────
    "Electrician":               {"sal_p0":  2,  "sal_p5":  4, "sal_p10":  7, "sal_p20": 12, "industry": "Construction",
                                  "skills": ["Wiring", "Troubleshooting", "Electrical Systems", "Safety", "Blueprint Reading", "Panel Installation"]},
    "Plumber":                   {"sal_p0":  2,  "sal_p5":  4, "sal_p10":  6, "sal_p20": 10, "industry": "Construction",
                                  "skills": ["Piping", "Welding", "Troubleshooting", "Blueprint Reading", "Maintenance", "Hydraulics"]},
    "Welder":                    {"sal_p0":  2,  "sal_p5":  4, "sal_p10":  7, "sal_p20": 12, "industry": "Construction",
                                  "skills": ["Welding", "Fabrication", "Blueprint Reading", "Safety", "Metalworking", "TIG/MIG Welding"]},
    "Carpenter":                 {"sal_p0":  2,  "sal_p5":  4, "sal_p10":  6, "sal_p20": 10, "industry": "Construction",
                                  "skills": ["Woodworking", "Framing", "Blueprint Reading", "Power Tools", "Safety", "Furniture Design"]},
    "HVAC Technician":           {"sal_p0":  2,  "sal_p5":  5, "sal_p10":  8, "sal_p20": 14, "industry": "Construction",
                                  "skills": ["HVAC Systems", "Troubleshooting", "Climate Control", "Safety", "Blueprint Reading", "Refrigeration"]},

    # ── Sales & Real Estate ──────────────────────────────────────────────────
    # Sales execs often get low base + commission; base ~4-5 LPA
    "Sales Executive":           {"sal_p0":  4,  "sal_p5":  9, "sal_p10": 16, "sal_p20": 28, "industry": "Retail",
                                  "skills": ["B2B", "Sales", "Negotiation", "CRM", "Lead Generation", "Cold Calling", "Salesforce"]},
    "Sales Manager":             {"sal_p0":  6,  "sal_p5": 14, "sal_p10": 25, "sal_p20": 42, "industry": "Retail",
                                  "skills": ["Sales", "Team Management", "CRM", "B2B", "Forecasting", "Negotiation", "Budget Management"]},
    # RE agent: mostly commission based; low fixed
    "Real Estate Agent":         {"sal_p0":  3,  "sal_p5":  8, "sal_p10": 18, "sal_p20": 40, "industry": "Retail",
                                  "skills": ["Real Estate", "Negotiation", "Sales", "Customer Service", "Marketing", "Property Valuation"]},
    "Store Manager":             {"sal_p0":  3,  "sal_p5":  7, "sal_p10": 12, "sal_p20": 20, "industry": "Retail",
                                  "skills": ["Inventory Management", "Customer Service", "Sales", "Team Leadership", "Merchandising", "Retail Analytics"]},

    # ── Research & Science ────────────────────────────────────────────────────
    "Research Scientist":        {"sal_p0":  7,  "sal_p5": 18, "sal_p10": 32, "sal_p20": 55, "industry": "Science",
                                  "skills": ["Research", "Machine Learning", "Python", "Data Analysis", "Academic Writing", "Statistical Modeling", "Experiment Design"]},
    "Bioinformatics Analyst":    {"sal_p0":  5,  "sal_p5": 11, "sal_p10": 20, "sal_p20": 35, "industry": "Science",
                                  "skills": ["Python", "R", "Genomics", "Biostatistics", "Data Analysis", "Linux", "Bioinformatics Tools", "NGS"]},
    "Chemist":                   {"sal_p0":  3,  "sal_p5":  7, "sal_p10": 12, "sal_p20": 20, "industry": "Science",
                                  "skills": ["Chemistry", "Research", "Lab Techniques", "Data Analysis", "Chromatography", "Spectroscopy", "GMP"]},
    "Physicist":                 {"sal_p0":  5,  "sal_p5": 11, "sal_p10": 20, "sal_p20": 35, "industry": "Science",
                                  "skills": ["Physics", "Research", "Mathematics", "Python", "Data Analysis", "Matlab", "Quantum Mechanics"]}
}

# ─────────────────────────────────────────────────────────────────────────────
#  LOCATIONS (Indian + Remote)
# ─────────────────────────────────────────────────────────────────────────────
LOCATIONS = ["Bangalore", "Pune", "Hyderabad", "Delhi", "Mumbai", "Chennai", "Kolkata", "Ahmedabad", "Remote"]
LOCATION_WEIGHTS = [0.25, 0.12, 0.13, 0.15, 0.12, 0.08, 0.05, 0.04, 0.06]

# Additive bonus over base (LPA) — location premium is smaller for lower-paying roles
LOC_BONUS_PCT = {
    "Bangalore": 0.18, "Delhi": 0.15, "Mumbai": 0.15,
    "Hyderabad": 0.10, "Pune": 0.10,
    "Chennai": 0.05, "Kolkata": -0.05, "Ahmedabad": -0.08,
    "Remote": 0.12
}

# ─────────────────────────────────────────────────────────────────────────────
#  COMPANIES per industry
# ─────────────────────────────────────────────────────────────────────────────
COMPANIES = {
    "IT":           ["Google", "Microsoft", "Amazon", "Meta", "TCS", "Infosys", "Wipro",
                     "Accenture", "Oracle", "Atlassian", "Flipkart", "Ola", "PhonePe",
                     "Zomato", "Freshworks", "Zoho", "PayPal", "SAP", "Swiggy", "CRED"],
    "Healthcare":   ["Apollo Hospitals", "Fortis Healthcare", "Max Healthcare",
                     "Manipal Hospitals", "Narayana Health", "Pfizer India",
                     "Novartis", "Johnson & Johnson", "Sanofi", "Abbott", "Roche India", "Sun Pharma"],
    "Finance":      ["Goldman Sachs", "JP Morgan", "Morgan Stanley", "HDFC Bank",
                     "ICICI Bank", "Axis Bank", "Standard Chartered", "BlackRock", "Deloitte",
                     "PwC", "EY", "KPMG", "Nomura", "Bajaj Finance", "Kotak Mahindra"],
    "Education":    ["IIT Bombay", "IIT Delhi", "IISc", "IIM Ahmedabad", "IIM Calcutta",
                     "NIT Trichy", "BITS Pilani", "Amity University", "Byju's", "Unacademy", "Vedantu"],
    "Engineering":  ["Larsen & Toubro", "Tata Motors", "Tata Steel", "Mahindra",
                     "Bharat Forge", "BHEL", "Siemens India", "Bosch India", "ABB India", "NTPC", "ISRO"],
    "Science":      ["ISRO", "DRDO", "CSIR", "DeepMind", "OpenAI", "Thermo Fisher",
                     "TIFR", "Bayer", "AstraZeneca India"],
    "Legal":        ["Cyril Amarchand Mangaldas", "AZB & Partners", "Khaitan & Co",
                     "Luthra & Luthra", "Shardul Amarchand", "DLA Piper India", "Anand & Anand"],
    "Design":       ["Adobe India", "Apple India", "Flipkart Design", "Zomato Design",
                     "Canva", "IDEO", "Airbnb India", "Dream11", "Urban Company"],
    "Operations":   ["Amazon India", "Flipkart", "Walmart India", "DHL India",
                     "Maersk India", "Reliance Retail", "DMart", "BigBasket", "McKinsey", "Bain"],
    "Marketing":    ["Ogilvy India", "Publicis India", "Leo Burnett", "Dentsu India",
                     "MullenLowe", "WPP India", "Wunderman Thompson", "HUL"],
    "Entertainment":["Disney India", "Netflix India", "Sony Pictures India",
                     "ZEE Entertainment", "Amazon Prime Video India", "T-Series", "Viacom18"],
    "Retail":       ["Reliance Retail", "D-Mart", "Shoppers Stop", "Big Bazaar",
                     "IKEA India", "Croma", "Amazon Retail", "Myntra", "Meesho"],
    "Construction": ["Larsen & Toubro", "DLF", "Shapoorji Pallonji", "Godrej Properties",
                     "Prestige Group", "Brigade Group", "Tata Projects", "NCC Limited"]
}

# Premium company adds 25% on top (FAANG / top-10 in India for each sector)
PREMIUM_COMPANIES = {
    "Google", "Microsoft", "Amazon", "Meta", "Goldman Sachs", "JP Morgan",
    "OpenAI", "DeepMind", "McKinsey", "BlackRock", "ISRO", "IIT Bombay",
    "IIM Ahmedabad", "Cyril Amarchand Mangaldas", "Bain"
}

# ─────────────────────────────────────────────────────────────────────────────
#  Weighted sampling — demand-driven roles appear 3x more
# ─────────────────────────────────────────────────────────────────────────────
HIGH_DEMAND_ROLES = {
    "Software Engineer", "Data Analyst", "Data Engineer", "Data Scientist",
    "ML Engineer", "AI Engineer", "Business Analyst", "Backend Developer",
    "Frontend Developer", "Full Stack Developer", "DevOps Engineer", "Cloud Engineer",
    "Doctor", "Nurse", "Teacher", "Professor",
    "Financial Analyst", "Chartered Accountant", "HR Manager", "Product Manager",
    "Project Manager", "Mechanical Engineer", "Civil Engineer",
    "Lawyer", "UX Designer", "Sales Executive", "Digital Marketing Manager"
}

def role_weight(role_name):
    return 3 if role_name in HIGH_DEMAND_ROLES else 1


def interp_salary(p0, p5, p10, p20, exp):
    """Piecewise-linear interpolation anchored on real market data points."""
    if exp <= 0:
        return p0
    elif exp <= 5:
        return p0 + (p5 - p0) * (exp / 5.0)
    elif exp <= 10:
        return p5 + (p10 - p5) * ((exp - 5) / 5.0)
    elif exp <= 20:
        return p10 + (p20 - p10) * ((exp - 10) / 10.0)
    else:
        # Slow growth after 20 yrs — ~2% per extra year, uncapped
        return p20 * (1 + (exp - 20) * 0.02)


def salary_for_row(profile, exp, num_skills, location, companies):
    """Return (sal_min, sal_max) based on market-anchored interpolation."""
    midpoint = interp_salary(
        profile["sal_p0"], profile["sal_p5"],
        profile["sal_p10"], profile["sal_p20"], exp
    )

    # Location premium/discount (additive percentage)
    loc_pct = LOC_BONUS_PCT.get(location, 0.0)
    midpoint *= (1 + loc_pct)

    # Premium company adds 25%
    comp_f = 1.0
    for c in companies:
        if c and any(p.lower() in c.lower() for p in PREMIUM_COMPANIES):
            comp_f = 1.25
            break
    midpoint *= comp_f

    # Skills add up to 8% (max at 5 skills = +8%)
    midpoint *= (1 + num_skills * 0.016)

    # Random variance ± 10%
    variance = random.uniform(0.90, 1.10)
    sal_min = midpoint * variance

    # sal_max = sal_min + 20% to 50% spread (realistic offer range)
    spread = random.uniform(1.20, 1.50)
    sal_max = sal_min * spread

    return round(max(sal_min, 1.0), 1), round(sal_max, 1)


def generate_dataset(num_records: int = 15000):
    data = []

    roles = list(PROFILES.keys())
    weights = [role_weight(r) for r in roles]
    probs = [w / sum(weights) for w in weights]

    TIER1_ROLES = {
        "Investment Banker", "Surgeon", "Doctor", "Lawyer", "Corporate Counsel",
        "Quant Analyst", "Radiologist", "Staff Engineer", "AI Engineer", "ML Engineer"
    }

    for _ in range(num_records):
        role = random.choices(roles, weights=probs, k=1)[0]
        profile = PROFILES[role]
        industry = profile["industry"]

        # Realistic experience distribution skewed towards early career
        exp = int(np.random.gamma(shape=2.2, scale=4.0))
        exp = min(max(exp, 0), 38)

        location = random.choices(LOCATIONS, weights=LOCATION_WEIGHTS, k=1)[0]

        # Skills
        pool = profile["skills"]
        num_skills = random.randint(1, min(5, len(pool)))
        chosen_skills = random.sample(pool, num_skills)
        chosen_skills += [""] * (5 - len(chosen_skills))

        # Companies
        available = COMPANIES.get(industry, COMPANIES["IT"])
        if exp == 0:
            num_comps = 0
        else:
            r = random.random()
            num_comps = 0 if r < 0.15 else (
                random.randint(1, 3) if r < 0.90
                else random.randint(4, min(5, len(available)))
            )
        chosen_comps = random.sample(available, min(num_comps, len(available)))
        chosen_comps += [""] * (5 - len(chosen_comps))

        sal_min, sal_max = salary_for_row(profile, exp, num_skills, location, chosen_comps)

        # Hard fresher cap — enforce realistic entry-level ceilings
        if exp == 0:
            fresher_ceil = 20.0 if role in TIER1_ROLES else 12.0
            sal_max = min(sal_max, fresher_ceil)
            sal_min = min(sal_min, fresher_ceil * 0.70)
            sal_min = max(sal_min, 1.5)

        data.append([
            role, exp, industry, location, sal_min, sal_max,
            chosen_skills[0], chosen_skills[1], chosen_skills[2],
            chosen_skills[3], chosen_skills[4],
            chosen_comps[0], chosen_comps[1], chosen_comps[2],
            chosen_comps[3], chosen_comps[4]
        ])

    df = pd.DataFrame(data, columns=[
        "job_title", "experience_years", "industry", "location",
        "salary_min_lpa", "salary_max_lpa",
        "skill_1", "skill_2", "skill_3", "skill_4", "skill_5",
        "company_1", "company_2", "company_3", "company_4", "company_5"
    ])

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salary_prediction_dataset.csv")
    df.to_csv(out_path, index=False)
    print(f"Dataset generated: {len(df):,} records across {df['job_title'].nunique()} roles")
    print(f"  Saved -> {out_path}")


if __name__ == "__main__":
    generate_dataset()
