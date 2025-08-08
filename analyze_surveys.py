#!/usr/bin/env python3
import pandas as pd
import json
import ast
from collections import Counter, defaultdict
import re

def parse_json_like_string(s):
    """Parse JSON-like strings from the CSV"""
    if pd.isna(s) or s == '' or s == '[]':
        return []
    
    # Handle cases where it's already parsed as a list
    if isinstance(s, list):
        return s
    
    # Clean up the string to make it valid JSON
    try:
        # Replace single quotes with double quotes for JSON parsing
        s = s.replace("'", '"')
        # Handle special cases
        s = s.replace('""', '"')
        # Parse as JSON
        return json.loads(s)
    except:
        try:
            # Try literal_eval for Python-like lists
            return ast.literal_eval(s.replace('"', "'"))
        except:
            # If all else fails, try to extract content manually
            if s.startswith('[') and s.endswith(']'):
                content = s[1:-1]
                if content.strip():
                    # Split by comma and clean up
                    items = [item.strip().strip('"').strip("'") for item in content.split('","') if item.strip()]
                    return [item.replace('""', '"') for item in items]
            return []

def parse_satisfaction_scores(s):
    """Parse satisfaction scores JSON"""
    if pd.isna(s) or s == '':
        return {}
    try:
        # Clean up the string
        s = s.replace("'", '"')
        return json.loads(s)
    except:
        return {}

def analyze_surveys():
    # Read the CSV file
    df = pd.read_csv('/Users/kumagai/workspace/sdgsfair-result/surveys.csv')
    
    print(f"=== SDGs FAIR SURVEY ANALYSIS REPORT ===")
    print(f"Total responses: {len(df)}")
    print(f"Survey period: {df['created_at'].min()} to {df['created_at'].max()}\n")
    
    # 1. DEMOGRAPHICS ANALYSIS
    print("=== 1. PARTICIPANT DEMOGRAPHICS ===\n")
    
    # Gender distribution
    gender_dist = df['gender'].value_counts()
    print("Gender Distribution:")
    for gender, count in gender_dist.items():
        percentage = (count / len(df)) * 100
        print(f"  {gender}: {count} ({percentage:.1f}%)")
    print()
    
    # Age distribution
    age_dist = df['age'].value_counts()
    print("Age Distribution:")
    for age, count in age_dist.items():
        percentage = (count / len(df)) * 100
        print(f"  {age}: {count} ({percentage:.1f}%)")
    print()
    
    # Occupation distribution
    occupation_dist = df['occupation'].value_counts()
    print("Occupation Distribution:")
    for occ, count in occupation_dist.items():
        percentage = (count / len(df)) * 100
        print(f"  {occ}: {count} ({percentage:.1f}%)")
    print()
    
    # Residence distribution
    residence_dist = df['residence'].value_counts()
    print("Residence Distribution:")
    for res, count in residence_dist.items():
        percentage = (count / len(df)) * 100
        print(f"  {res}: {count} ({percentage:.1f}%)")
    print()
    
    # 2. VISIT PURPOSE ANALYSIS
    print("=== 2. VISIT PURPOSE ANALYSIS ===\n")
    
    all_purposes = []
    for purposes in df['visit_purpose_list']:
        parsed_purposes = parse_json_like_string(purposes)
        all_purposes.extend(parsed_purposes)
    
    purpose_counts = Counter(all_purposes)
    print("Visit Purposes:")
    for purpose, count in purpose_counts.most_common():
        percentage = (count / len(df)) * 100
        print(f"  {purpose}: {count} ({percentage:.1f}%)")
    print()
    
    # 3. SDGs GOALS INTEREST ANALYSIS
    print("=== 3. SDGs GOALS INTEREST ANALYSIS ===\n")
    
    sdg_interest = df['interested_sdgs_goal'].value_counts()
    print("Most Interested SDGs Goals:")
    for goal, count in sdg_interest.items():
        percentage = (count / len(df)) * 100
        print(f"  {goal}: {count} ({percentage:.1f}%)")
    print()
    
    # 4. CURRENT SDGs ACTIONS ANALYSIS
    print("=== 4. CURRENT SDGs ACTIONS ANALYSIS ===\n")
    
    all_actions = []
    for actions in df['current_sdgs_actions']:
        parsed_actions = parse_json_like_string(actions)
        all_actions.extend(parsed_actions)
    
    action_counts = Counter(all_actions)
    print("Current SDGs Actions (Top 10):")
    for action, count in action_counts.most_common(10):
        percentage = (count / len(df)) * 100
        print(f"  {action}: {count} ({percentage:.1f}%)")
    print()
    
    # 5. SDGs ACTION TRIGGERS
    print("=== 5. SDGs ACTION TRIGGERS ===\n")
    
    trigger_counts = df['sdgs_action_trigger'].value_counts().head(10)
    print("Top SDGs Action Triggers:")
    for trigger, count in trigger_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {trigger}: {count} ({percentage:.1f}%)")
    print()
    
    # 6. FUTURE SDGs INTEREST
    print("=== 6. FUTURE SDGs INTEREST ===\n")
    
    future_interest = df['future_sdgs_interest'].value_counts()
    print("Future SDGs Interest:")
    for interest, count in future_interest.items():
        percentage = (count / len(df)) * 100
        print(f"  {interest}: {count} ({percentage:.1f}%)")
    print()
    
    # 7. SATISFACTION RATINGS ANALYSIS
    print("=== 7. SATISFACTION RATINGS ANALYSIS ===\n")
    
    # Parse all satisfaction scores
    all_satisfaction = defaultdict(list)
    for satisfaction_str in df['content_satisfaction']:
        satisfaction_dict = parse_satisfaction_scores(satisfaction_str)
        for category, score in satisfaction_dict.items():
            try:
                all_satisfaction[category].append(int(score))
            except:
                pass
    
    print("Average Satisfaction Scores (1-5 scale):")
    for category, scores in all_satisfaction.items():
        if scores:
            avg_score = sum(scores) / len(scores)
            print(f"  {category}: {avg_score:.2f} (n={len(scores)})")
    print()
    
    # 8. MEMORABLE BOOTHS ANALYSIS
    print("=== 8. MEMORABLE BOOTHS ANALYSIS ===\n")
    
    booth_mentions = df['memorable_booth'].value_counts().head(10)
    print("Most Memorable Booths (Top 10):")
    for booth, count in booth_mentions.items():
        if pd.notna(booth) and booth != '':
            percentage = (count / len(df[df['memorable_booth'].notna()])) * 100
            print(f"  {booth}: {count} ({percentage:.1f}%)")
    print()
    
    # 9. LEARNING MOMENTS
    print("=== 9. LEARNING MOMENTS ===\n")
    
    learning_yes = df['learning_moments'].value_counts()
    print("Had Learning Moments:")
    for response, count in learning_yes.items():
        percentage = (count / len(df)) * 100
        print(f"  {response}: {count} ({percentage:.1f}%)")
    print()
    
    # 10. OKAYAMA FOCUS AREAS
    print("=== 10. OKAYAMA FOCUS AREAS ===\n")
    
    all_focus_areas = []
    for areas in df['okayama_focus_areas']:
        parsed_areas = parse_json_like_string(areas)
        all_focus_areas.extend(parsed_areas)
    
    focus_counts = Counter(all_focus_areas)
    print("Priority Focus Areas for Okayama:")
    for area, count in focus_counts.most_common():
        if area:  # Skip empty strings
            percentage = (count / len(df)) * 100
            print(f"  {area}: {count} ({percentage:.1f}%)")
    print()
    
    # 11. SDGs CHALLENGES
    print("=== 11. SDGs CHALLENGES (Key Themes) ===\n")
    
    # Analyze challenges text for common themes
    challenges_text = df['sdgs_challenges'].dropna().str.lower()
    
    # Count common keywords/themes
    challenge_themes = {
        '意識': len([t for t in challenges_text if '意識' in str(t)]),
        '認知': len([t for t in challenges_text if '認知' in str(t)]),
        '教育': len([t for t in challenges_text if '教育' in str(t)]),
        'ゴミ': len([t for t in challenges_text if 'ごみ' in str(t) or 'ゴミ' in str(t)]),
        '環境': len([t for t in challenges_text if '環境' in str(t)]),
        '個人': len([t for t in challenges_text if '個人' in str(t)]),
        '温暖化': len([t for t in challenges_text if '温暖化' in str(t)]),
        '海ゴミ': len([t for t in challenges_text if '海ごみ' in str(t) or '海ゴミ' in str(t)]),
        '食品ロス': len([t for t in challenges_text if 'フードロス' in str(t) or '食品ロス' in str(t)])
    }
    
    print("Common Challenge Themes:")
    for theme, count in sorted(challenge_themes.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(challenges_text)) * 100
        print(f"  {theme}: {count} mentions ({percentage:.1f}%)")
    print()
    
    # 12. IMPROVEMENTS SUGGESTIONS
    print("=== 12. IMPROVEMENTS ANALYSIS ===\n")
    
    improvements = df['improvements'].dropna()
    print(f"Total improvement suggestions: {len(improvements)}")
    print(f"Percentage of respondents who provided suggestions: {(len(improvements)/len(df))*100:.1f}%")
    print()
    
    # Sample of improvement suggestions
    if len(improvements) > 0:
        print("Sample Improvement Suggestions:")
        for i, suggestion in enumerate(improvements.head(5)):
            if suggestion and suggestion.strip():
                print(f"  {i+1}. {suggestion[:100]}...")
        print()
    
    # 13. KEY INSIGHTS AND TRENDS
    print("=== 13. KEY INSIGHTS AND TRENDS ===\n")
    
    # Age group insights
    young_participants = len(df[df['age'].isin(['中学生以下', '高校生', '大学生', '20代'])])
    adult_participants = len(df[df['age'].isin(['30代', '40代', '50代'])])
    senior_participants = len(df[df['age'].isin(['60代', '70代以上'])])
    
    print("Age Group Analysis:")
    print(f"  Young participants (≤20s): {young_participants} ({(young_participants/len(df))*100:.1f}%)")
    print(f"  Adult participants (30s-50s): {adult_participants} ({(adult_participants/len(df))*100:.1f}%)")
    print(f"  Senior participants (≥60s): {senior_participants} ({(senior_participants/len(df))*100:.1f}%)")
    print()
    
    # Education-related occupations
    education_related = len(df[df['occupation'].isin(['学生', '教職員'])])
    print(f"Education-related participants: {education_related} ({(education_related/len(df))*100:.1f}%)")
    print()
    
    # High satisfaction indicators
    high_satisfaction_overall = len([score for satisfaction_str in df['content_satisfaction'] 
                                   for category, score in parse_satisfaction_scores(satisfaction_str).items()
                                   if category == '全体' and int(score) >= 4])
    
    print(f"High overall satisfaction (≥4/5): {high_satisfaction_overall} responses")
    print()
    
    # Most common current actions
    print("Top 5 Most Common Current SDGs Actions:")
    for i, (action, count) in enumerate(action_counts.most_common(5), 1):
        print(f"  {i}. {action}: {count} participants")
    print()
    
    # Regional participation
    okayama_inside = len(df[df['residence'] == '岡山県内'])
    okayama_outside = len(df[df['residence'] == '岡山県外'])
    
    print("Regional Participation:")
    print(f"  Okayama Prefecture residents: {okayama_inside} ({(okayama_inside/len(df))*100:.1f}%)")
    print(f"  Outside Okayama Prefecture: {okayama_outside} ({(okayama_outside/len(df))*100:.1f}%)")
    print()
    
    print("=== ANALYSIS COMPLETE ===")
    
if __name__ == "__main__":
    analyze_surveys()