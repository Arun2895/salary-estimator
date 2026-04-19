def get_experience_level(exp):
    if exp <= 2:
        return 4
    elif exp <= 5:
        return 6
    elif exp <= 8:
        return 8
    else:
        return 10


def get_skill_level(skill_score):
    # skill_score is the sum of importance scores, max ~50 for 5 skills
    if skill_score <= 5:
        return 2  # No skills or basic
    elif skill_score <= 15:
        return 4  # 1-2 skills
    elif skill_score <= 25:
        return 6  # 2-3 skills
    elif skill_score <= 35:
        return 8  # 3-4 skills
    else:
        return 10 # 4-5 high value skills


def fuzzy_adjustment(base_salary, exp_level, skill_level, industry_score, location_score, company_score=1):
    # Base factor has been shifted to favor Skill much more heavily (0.7 weight)
    # Company score also adds a multiplier
    
    skill_factor = (skill_level / 10)
    exp_factor = (exp_level / 10)
    
    # Final factor reflects the prompt: "no with skill the salary should obviously vary"
    factor = (
        0.7 * skill_factor +
        0.2 * exp_factor +
        0.05 * (industry_score / 3) +
        0.05 * (location_score / 3)
    )

    # Apply company tier multiplier (1 to 4)
    # Tier 4 (Best) = 4, Tier 1 (Base) = 1
    company_multiplier = 1.0 + (company_score - 1) * 0.15 # Max 45% boost for top companies
    
    adjusted_salary = base_salary * (0.5 + factor) * company_multiplier
    
    return adjusted_salary