# Nonprofit Data Analysis Assessment
 
## Overview
 
This project analyzes a survey of respondents in Colorado and Montana to understand how aware people are of environmental policy and organizations, which environmental issues matter most to them locally, and how likely they are to donate to an environmental organization.
 
**Findings:** Awareness and giving intent differ by audience. Montana trails Colorado on IRA awareness, women are more open to giving than men, and familiarity with environmental groups goes most closely with willingness to donate.
 
## File Structure

```
├── README.md
├── requirements.txt              # Python dependencies
├── data/
│   ├── raw/
│   │   ├── survey_data.csv       # raw survey responses
│   │   └── codelist.csv          # codebook: question text and response labels (1-5)
│   ├── clean/
│   │   └── clean_data.csv        # cleaned data (output of notebook 01)
│   └── data.csv                  # [describe or remove: unclear how this differs from raw/clean]
├── notebooks/
│   ├── 01_data_cleaning.ipynb    # recode, handle Don't know / Unsure, build clean data
│   ├── 02_exploratory_analysis.ipynb  # crosstabs and grouped bar charts by state and sex
│   └── 03_modeling.ipynb         # significance tests, joint models, Spearman correlations
├── figures/
│   ├── takeaway_1a.svg           # IRA awareness by state
│   ├── takeaway_2a.svg           # donation likelihood by sex
│   └── takeaway_3a.svg           # donation likelihood by awareness
└── src/
    └── viz_theme.py              # shared chart theme (colors, chart width)
```

## Methodology
 
**Tools:** Python (pandas, numpy, SciPy, statsmodels, Altair).
 
**Cleaning**
- "Don't know" (Q1-Q3) and "Unsure" (Q5) answers, coded 5, were treated as missing in the statistical tests. They are not a level of awareness or likelihood, so keeping them on the scale would distort comparisons.
- Q4 (most important environmental issue) was treated as categorical and never averaged.
 
**Analysis**
- **Crosstabs + Grouped Bar Charts** for each question by state and by sex, shown as a percentage of each group.
- **Cramer's V** for each question by state and by sex, with Holm correction for multiple comparisons.
- **Mann-Whitney U Test** for the ordinal questions (Q1-Q3, Q5), because the gaps between response levels are not equal and samples are small.
- **Logistic Models with Interactions** with state and sex entered together, using a top-2 split (very or somewhat aware/donate). This separates state effects from sex effects, since the two overlap.
- **Spearman correlations** between awareness (Q1-Q3) and donation intent (Q5).
 
## Questions
 
**Survey questions**
 
| Item | Question | Response scale |
|---|---|---|
| Q1 | Familiarity with the Inflation Reduction Act (IRA) | Very Aware to Not aware at all, Don't know |
| Q2 | Familiarity with Green Machine | Very Aware to Not aware at all, Don't know |
| Q3 | Familiarity with WWF, NRDC, or the Sierra Club | Very Aware to Not aware at all, Don't know |
| Q4 | Most important environmental issue in your local area | Climate Change, Environmental Justice, Clean Air & Water, Land & Wildlife, Something Else / Don't Know |
| Q5 | Likelihood of donating to an environmental organization in the next year | Extremely Likely to Not likely, Unsure |


## Results
 
1. **Montana trails Colorado on IRA awareness.** 61% of Colorado respondents are very or somewhat aware of the IRA, compared with 16% in Montana. Montana's odds of being aware are about 85% lower (OR = 0.15, p < .001), and the gap holds for both women and men.

2. **Women are more open to giving than men.** 44% of women are extremely or very likely to donate, compared with 19% of men. Men's odds are about 70% lower after accounting for state (OR = 0.30, p = .030). Women were also more aware of Green Machine (OR = 0.36 for men, p = .029).

3. **Awareness goes with giving, most strongly for environmental organizations.** People who know the major groups are 34 points more likely to say they will donate. Spearman correlations confirm associations between donation intent and degree of awareness.

4. **Priorities differ by sex.** The sex difference in top environmental issue is significant (p = .006).


## Limitations
 
Small samples and associations rather than causal claims. Results describe the sampled survey respondents and not the populations of Colorado and Montana.
 

 