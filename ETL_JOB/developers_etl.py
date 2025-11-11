import pandas as pd
import numpy as np

# Optional helper for country->continent mapping
try:
    import country_converter as coco   # pip install country_converter
    cc = coco.CountryConverter()
    use_cc = True
except Exception:
    use_cc = False
    # minimal fallback dictionary for common countries (expand as needed)
    FALLBACK_CONTINENT = {
        'United States': 'North America', 'India': 'Asia', 'United Kingdom': 'Europe',
        'Germany': 'Europe', 'France': 'Europe', 'Canada': 'North America',
        'Brazil': 'South America', 'Australia': 'Oceania', 'China': 'Asia',
        'Japan': 'Asia', 'Russia': 'Europe', 'Netherlands': 'Europe',
        # ... add more as required
    }

# ------------- 1) load data ---------------
df = pd.read_csv("survey_results_public.csv", low_memory=False)  # adjust path if needed
# Quick look
print("Rows, cols:", df.shape)


# Sanitize column names if needed (some CSVs have different header names)
cols = df.columns.tolist()
required = ['Age1stCode','Country','LanguageWorkedWith','LanguageDesireNextYear',
            'ConvertedComp','Gender','Hobbyist','JobSat','CareerSat']
print("Has required columns:", {c: c in df.columns for c in required})

# ------------- helpers ---------------------
def normalize_age(x):
    # Age1stCode sometimes contains strings or ranges like 'Younger than 5' or 'Older than 85'
    # Convert to numeric where possible, or NaN.
    if pd.isna(x): 
        return np.nan
    if isinstance(x, (int,float)): 
        return x
    s = str(x).strip()
    # handle common forms:
    s = s.replace('+','').replace('younger than','').replace('older than','')
    s = s.replace('Younger than', '').replace('Older than','').strip()
    try:
        return float(s)
    except:
        # if format like '5 years' or other text, try digits
        import re
        m = re.search(r'(\d+)', s)
        if m: 
            return float(m.group(1))
        return np.nan

def normalize_gender(g):
    # RULE from assignment:
    # If record has singular/atomic value as MAN or WOMAN -> treat as such.
    # If ambiguous value -> OTHERS.
    if pd.isna(g):
        return 'OTHERS'
    s = str(g).strip().lower()
    # common singular forms
    man_tokens = {'man','male','m','cis man','cis male','man ' }
    woman_tokens = {'woman','female','f','cis woman','cis female','woman '}
    # many survey answers are long (e.g., "Man; Non-binary, genderqueer")
    # If the cell contains ONLY a token from man_tokens (ignoring case/punctuation) -> MAN
    # Similarly for WOMAN. Otherwise -> OTHERS
    # To robustly check, split on common separators
    parts = [p.strip().lower() for p in re_split_gender(s)]
    # remove empty
    parts = [p for p in parts if p]
    if len(parts) == 1:
        p = parts[0]
        if p in man_tokens or p.startswith('man') or p.startswith('male'):
            return 'MAN'
        if p in woman_tokens or p.startswith('woman') or p.startswith('female'):
            return 'WOMAN'
    return 'OTHERS'

def re_split_gender(s):
    # split on common delimiters
    import re
    return re.split(r'[;,/|&\n]+', s)

def country_to_continent(country):
    if use_cc:
        try:
            # coco returns continent codes; convert to names
            code = cc.convert(names=country, to='continent')
            # sometimes result 'not found' -> map to NaN
            if code in ['not found', None, 'nan']:
                return np.nan
            return code
        except:
            return np.nan
    else:
        return FALLBACK_CONTINENT.get(country, np.nan)

# ------------- PREPROCESS ------------------
# 1. Age when wrote first code -> numeric
df['Age1stCode_num'] = df['Age1stCode'].apply(normalize_age)

# 2. Normalize gender
import re
df['Gender_norm'] = df['Gender'].apply(lambda x: normalize_gender(x) if not pd.isna(x) else 'OTHERS')

# 3. Map countries -> continents
if use_cc:
    # country_converter continent returns full names (e.g., 'Asia', 'Europe', 'Africa')
    df['Continent'] = df['Country'].apply(lambda c: country_to_continent(c))
else:
    df['Continent'] = df['Country'].apply(lambda c: country_to_continent(c))

# 4. Language columns: split into lists
# The survey stores multiple languages as semicolon-separated or ';' or ',' depending.
def split_lang_cell(cell):
    if pd.isna(cell): return []
    # common separators ; , |
    parts = re.split(r'[;,|/]+', str(cell))
    return [p.strip() for p in parts if p.strip()]

df['LangWorked_list'] = df['LanguageWorkedWith'].apply(split_lang_cell)
df['LangDesire_list'] = df['LanguageDesireNextYear'].apply(split_lang_cell)

# ------------- Q1: average age of developers when they wrote first line of code -------------
q1_df = df['Age1stCode_num'].dropna()
avg_age_first_code = q1_df.mean()
median_age_first_code = q1_df.median()
print("Q1 - Average Age1stCode:", avg_age_first_code, "Median:", median_age_first_code)

# ------------- Q2: percentage of developers who knew Python in each country -------------
# We'll check if 'Python' appears in LangWorked_list
df['Knows_Python'] = df['LangWorked_list'].apply(lambda lst: 'Python' in [p.strip() for p in lst])
# Group by country and compute percent:
q2 = df.groupby('Country').agg(
    total_respondents = ('Knows_Python','size'),
    python_count = ('Knows_Python','sum')
).reset_index()
q2['pct_python'] = q2['python_count'] / q2['total_respondents'] * 100
# Sort example:
q2_sorted = q2.sort_values('pct_python', ascending=False)
# Save
q2_sorted.to_csv('q2_pct_python_by_country.csv', index=False)
print("Q2 Answer saved to q2_pct_python_by_country.csv")

# ------------- Q3: average salary of developers based on the continent -------------
# Use 'ConvertedComp' (may be in USD); drop NaNs
salary_df = df[['Continent','ConvertedComp']].copy()
salary_df = salary_df[~salary_df['ConvertedComp'].isna() & ~salary_df['Continent'].isna()]
# Some extremely large outliers may exist; you can clip or take median
q3 = salary_df.groupby('Continent').agg(
    count=('ConvertedComp','size'),
    mean_salary=('ConvertedComp','mean'),
    median_salary=('ConvertedComp','median')
).reset_index()
q3.to_csv('q3_mean_salary_by_continent.csv', index=False)
print("Q3 Answer saved to q3_mean_salary_by_continent.csv")

# ------------- Q4: most desired programming language for 2020 -------------
# Use LanguageDesireNextYear column to find the single language with highest appearances
# Explode lists and count
desire_exploded = df[['LangDesire_list']].explode('LangDesire_list')
desire_exploded['LangDesire_list'] = desire_exploded['LangDesire_list'].str.strip()
lang_counts = desire_exploded['LangDesire_list'].value_counts().reset_index()
lang_counts.columns = ['Language','Count']
most_desired_language = lang_counts.iloc[0]['Language']
print("Q4 - Most desired language for 2020:", most_desired_language)
lang_counts.to_csv('q4_language_desire_counts.csv', index=False)
print("Q4 Answer saved to q4_language_desire_counts.csv")

# ------------- Q5: people who code as a hobby by gender and continent -------------
# Keep only rows where Hobbyist == 'Yes' (or case-insensitive)
df['Hobbyist_bool'] = df['Hobbyist'].astype(str).str.strip().str.lower() == 'yes'
q5 = df[df['Hobbyist_bool']].groupby(['Continent','Gender_norm']).size().reset_index(name='count')
# Also get percent within continent
continent_totals = df.groupby('Continent').size().reset_index(name='continent_total')
q5 = q5.merge(continent_totals, on='Continent', how='left')
q5['pct_of_continent'] = q5['count'] / q5['continent_total'] * 100
q5.to_csv('q5_hobbyist_by_gender_continent.csv', index=False)
print("Q5 Answer saved to q5_hobbyist_by_gender_continent.csv") 

# ------------- Q6: job and career satisfaction by gender and continent -------------
# JobSat and CareerSat are strings like 'Slightly satisfied', 'Very satisfied', etc.
# We'll compute counts and percentages for each satisfaction level grouped by Continent and Gender_norm
sat_df = df[['Continent','Gender_norm','JobSat','CareerSat']].copy()
# normalise NA
sat_df['JobSat'] = sat_df['JobSat'].fillna('NoResponse')
sat_df['CareerSat'] = sat_df['CareerSat'].fillna('NoResponse')

# JobSat distribution
q6_job = sat_df.groupby(['Continent','Gender_norm','JobSat']).size().reset_index(name='count')
# compute percent within (Continent, Gender_norm) group
group_totals = sat_df.groupby(['Continent','Gender_norm']).size().reset_index(name='group_total')
q6_job = q6_job.merge(group_totals, on=['Continent','Gender_norm'], how='left')
q6_job['pct'] = q6_job['count'] / q6_job['group_total'] * 100
q6_job.to_csv('q6_job_satisfaction_by_gender_continent.csv', index=False)

# CareerSat distribution
q6_career = sat_df.groupby(['Continent','Gender_norm','CareerSat']).size().reset_index(name='count')
q6_career = q6_career.merge(group_totals, on=['Continent','Gender_norm'], how='left')
q6_career['pct'] = q6_career['count'] / q6_career['group_total'] * 100
q6_career.to_csv('q6_career_satisfaction_by_gender_continent.csv', index=False)
print("Q6 Answers saved to q6_job_satisfaction_by_gender_continent.csv and q6_career_satisfaction_by_gender_continent.csv")

print("DONE. CSVs created for each question's report.")
