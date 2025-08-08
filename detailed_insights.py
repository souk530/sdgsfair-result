#!/usr/bin/env python3
import pandas as pd
import json
import ast
from collections import Counter, defaultdict

def parse_json_like_string(s):
    """Parse JSON-like strings from the CSV"""
    if pd.isna(s) or s == '' or s == '[]':
        return []
    
    if isinstance(s, list):
        return s
    
    try:
        s = s.replace("'", '"')
        s = s.replace('""', '"')
        return json.loads(s)
    except:
        try:
            return ast.literal_eval(s.replace('"', "'"))
        except:
            if s.startswith('[') and s.endswith(']'):
                content = s[1:-1]
                if content.strip():
                    items = [item.strip().strip('"').strip("'") for item in content.split('","') if item.strip()]
                    return [item.replace('""', '"') for item in items]
            return []

def detailed_analysis():
    df = pd.read_csv('/Users/kumagai/workspace/sdgsfair-result/surveys.csv')
    
    print("=== DETAILED QUALITATIVE INSIGHTS ===\n")
    
    # Learning moments analysis
    print("=== NOTABLE LEARNING MOMENTS ===")
    learning_moments = df[df['learning_moments_detail'].notna() & (df['learning_moments_detail'] != '')]['learning_moments_detail']
    print(f"Total detailed learning moments recorded: {len(learning_moments)}")
    print("\nSample Learning Moments:")
    for i, moment in enumerate(learning_moments.head(10), 1):
        print(f"{i}. {moment[:150]}...")
    print()
    
    # SDGs challenges detailed analysis
    print("=== DETAILED SDGs CHALLENGES ===")
    challenges = df[df['sdgs_challenges'].notna() & (df['sdgs_challenges'] != '')]['sdgs_challenges']
    print(f"Total challenges mentioned: {len(challenges)}")
    print("\nKey Challenge Responses:")
    
    # Group similar challenges
    awareness_challenges = []
    environmental_challenges = []
    social_challenges = []
    implementation_challenges = []
    
    for challenge in challenges:
        challenge_lower = str(challenge).lower()
        if '意識' in challenge_lower or '認知' in challenge_lower or 'sdgs' in challenge_lower:
            awareness_challenges.append(challenge)
        elif 'ごみ' in challenge_lower or '環境' in challenge_lower or '温暖化' in challenge_lower:
            environmental_challenges.append(challenge)
        elif '格差' in challenge_lower or '貧困' in challenge_lower or '平等' in challenge_lower:
            social_challenges.append(challenge)
        else:
            implementation_challenges.append(challenge)
    
    print("Awareness & Education Challenges:")
    for challenge in awareness_challenges[:5]:
        print(f"  • {challenge[:100]}...")
    
    print("\nEnvironmental Challenges:")
    for challenge in environmental_challenges[:5]:
        print(f"  • {challenge[:100]}...")
    
    print("\nImplementation & Action Challenges:")
    for challenge in implementation_challenges[:5]:
        print(f"  • {challenge[:100]}...")
    print()
    
    # Improvement suggestions analysis
    print("=== IMPROVEMENT SUGGESTIONS ===")
    improvements = df[df['improvements'].notna() & (df['improvements'] != '')]['improvements']
    print(f"Total improvement suggestions: {len(improvements)}")
    print("\nKey Improvement Suggestions:")
    for i, suggestion in enumerate(improvements, 1):
        print(f"{i}. {suggestion[:120]}...")
    print()
    
    # Future SDGs actions analysis
    print("=== FUTURE SDGs ACTIONS ===")
    future_actions = df[df['future_sdgs_actions'].notna() & (df['future_sdgs_actions'] != '')]['future_sdgs_actions']
    print(f"Total future action commitments: {len(future_actions)}")
    print("\nSample Future Action Commitments:")
    for i, action in enumerate(future_actions.head(15), 1):
        print(f"{i}. {action[:100]}...")
    print()
    
    # Cross-analysis: Age vs SDGs Interest
    print("=== AGE GROUP SDGs PREFERENCES ===")
    
    young_group = df[df['age'].isin(['中学生以下', '高校生', '大学生', '20代'])]
    adult_group = df[df['age'].isin(['30代', '40代', '50代'])]
    senior_group = df[df['age'].isin(['60代', '70代以上'])]
    
    print("Young Group (≤20s) Top SDGs Interests:")
    young_sdgs = young_group['interested_sdgs_goal'].value_counts().head(5)
    for goal, count in young_sdgs.items():
        print(f"  {goal}: {count}")
    
    print("\nAdult Group (30s-50s) Top SDGs Interests:")
    adult_sdgs = adult_group['interested_sdgs_goal'].value_counts().head(5)
    for goal, count in adult_sdgs.items():
        print(f"  {goal}: {count}")
    
    print("\nSenior Group (≥60s) Top SDGs Interests:")
    senior_sdgs = senior_group['interested_sdgs_goal'].value_counts().head(5)
    for goal, count in senior_sdgs.items():
        print(f"  {goal}: {count}")
    print()
    
    # Action trigger analysis by age
    print("=== SDGs ACTION TRIGGERS BY AGE GROUP ===")
    
    print("Young Group Action Triggers:")
    young_triggers = young_group['sdgs_action_trigger'].value_counts().head(5)
    for trigger, count in young_triggers.items():
        print(f"  {trigger}: {count}")
    
    print("\nAdult Group Action Triggers:")
    adult_triggers = adult_group['sdgs_action_trigger'].value_counts().head(5)
    for trigger, count in adult_triggers.items():
        print(f"  {trigger}: {count}")
    
    print("\nSenior Group Action Triggers:")
    senior_triggers = senior_group['sdgs_action_trigger'].value_counts().head(5)
    for trigger, count in senior_triggers.items():
        print(f"  {trigger}: {count}")
    print()
    
    # Satisfaction correlation analysis
    print("=== SATISFACTION PATTERNS ===")
    
    def parse_satisfaction_scores(s):
        if pd.isna(s) or s == '':
            return {}
        try:
            s = s.replace("'", '"')
            return json.loads(s)
        except:
            return {}
    
    # Calculate satisfaction by visit purpose
    purposes_satisfaction = defaultdict(list)
    for idx, row in df.iterrows():
        purposes = parse_json_like_string(row['visit_purpose_list'])
        satisfaction = parse_satisfaction_scores(row['content_satisfaction'])
        if '全体' in satisfaction:
            try:
                overall_score = int(satisfaction['全体'])
                for purpose in purposes:
                    purposes_satisfaction[purpose].append(overall_score)
            except:
                pass
    
    print("Average Satisfaction by Visit Purpose:")
    for purpose, scores in purposes_satisfaction.items():
        if scores:
            avg_score = sum(scores) / len(scores)
            print(f"  {purpose}: {avg_score:.2f} (n={len(scores)})")
    print()
    
    # Regional insights
    print("=== REGIONAL INSIGHTS ===")
    
    okayama_internal = df[df['residence'] == '岡山県内']
    okayama_external = df[df['residence'] == '岡山県外']
    
    print("Okayama Internal vs External Participants:")
    print(f"Internal participants: {len(okayama_internal)} ({(len(okayama_internal)/len(df))*100:.1f}%)")
    print(f"External participants: {len(okayama_external)} ({(len(okayama_external)/len(df))*100:.1f}%)")
    
    print("\nTop residence details (Okayama Internal):")
    internal_details = okayama_internal['residence_detail'].value_counts().head(10)
    for location, count in internal_details.items():
        if pd.notna(location):
            print(f"  {location}: {count}")
    
    print("\nExternal participants locations:")
    external_details = okayama_external['residence_detail'].value_counts()
    for location, count in external_details.items():
        if pd.notna(location):
            print(f"  {location}: {count}")
    print()
    
    print("=== SUMMARY STATISTICS ===")
    print(f"Total survey responses analyzed: {len(df)}")
    print(f"Response rate for detailed feedback: {(len(df[df['sdgs_challenges'].notna()])/len(df))*100:.1f}%")
    print(f"Learning engagement rate: {(len(df[df['learning_moments'] == 'はい'])/len(df))*100:.1f}%")
    print(f"Future commitment rate: {(len(df[df['future_sdgs_interest'] == 'はい'])/len(df))*100:.1f}%")
    print(f"High satisfaction rate (≥4/5): {(len([1 for _, row in df.iterrows() for cat, score in parse_satisfaction_scores(row['content_satisfaction']).items() if cat == '全体' and int(score) >= 4])/len(df))*100:.1f}%")

if __name__ == "__main__":
    detailed_analysis()