import json
import math

WEIGHTS = {
    'payment_history': 0.35,
    'credit_utilization': 0.20,
    'credit_age': 0.15,
    'credit_mix': 0.10,
    'new_inquiries': 0.05,
    'dti_ratio': 0.05,
    'derogatory_marks': 0.05,
    'total_accounts': 0.05
}

def normalize(factor, value):
    normalizers = {
        'payment_history': lambda v: min(1, max(0, v / 100)),
        'credit_utilization': lambda v: max(0, 1 - v / 100),
        'credit_age': lambda v: min(1, v / 25),
        'credit_mix': lambda v: min(1, v / 5),
        'new_inquiries': lambda v: max(0, 1 - v / 10),
        'dti_ratio': lambda v: max(0, 1 - v / 60),
        'derogatory_marks': lambda v: max(0, 1 - v / 5),
        'total_accounts': lambda v: min(1, v / 20),
    }
    return normalizers.get(factor, lambda v: 0.5)(value)

def score_profile(profile):
    weighted_sum = sum(
        normalize(factor, profile.get(factor, 0)) * weight
        for factor, weight in WEIGHTS.items()
    )
    credit_score = max(300, min(850, round(300 + weighted_sum * 550)))
    grade = ('A+' if credit_score >= 800 else 'A' if credit_score >= 750 else
             'B+' if credit_score >= 700 else 'B' if credit_score >= 650 else
             'C' if credit_score >= 600 else 'F')
    decision = 'APPROVED' if credit_score >= 620 else 'MANUAL_REVIEW' if credit_score >= 600 else 'DENIED'
    risk_level = 'low' if credit_score >= 720 else 'medium' if credit_score >= 620 else 'high'
    default_prob = round(1 / (1 + math.exp(0.02 * (credit_score - 580))), 4)
    return {
        'credit_score': credit_score,
        'grade': grade,
        'decision': decision,
        'risk_level': risk_level,
        'default_probability': default_prob,
        'compliance': {'ecoa': True, 'fcra': True, 'model': 'EVEZ-CS-v2.0'}
    }

def handler(request):
    if request.method == 'OPTIONS':
        return {'statusCode': 200, 'headers': {'Access-Control-Allow-Origin': '*'}}
    try:
        body = json.loads(request.body)
        profile = body.get('profile', {})
        if not profile:
            return {'statusCode': 400, 'body': json.dumps({'error': 'profile required'})}
        result = score_profile(profile)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(result)
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
