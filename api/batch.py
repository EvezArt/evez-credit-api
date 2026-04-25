import json
import math

WEIGHTS = {
    'payment_history': 0.35, 'credit_utilization': 0.20, 'credit_age': 0.15,
    'credit_mix': 0.10, 'new_inquiries': 0.05, 'dti_ratio': 0.05,
    'derogatory_marks': 0.05, 'total_accounts': 0.05
}

def normalize(factor, value):
    fns = {
        'payment_history': lambda v: min(1, max(0, v/100)),
        'credit_utilization': lambda v: max(0, 1-v/100),
        'credit_age': lambda v: min(1, v/25),
        'credit_mix': lambda v: min(1, v/5),
        'new_inquiries': lambda v: max(0, 1-v/10),
        'dti_ratio': lambda v: max(0, 1-v/60),
        'derogatory_marks': lambda v: max(0, 1-v/5),
        'total_accounts': lambda v: min(1, v/20),
    }
    return fns.get(factor, lambda v: 0.5)(value)

def score_one(profile):
    s = sum(normalize(f, profile.get(f, 0)) * w for f, w in WEIGHTS.items())
    sc = max(300, min(850, round(300 + s * 550)))
    return {
        'credit_score': sc,
        'grade': 'A+' if sc>=800 else 'A' if sc>=750 else 'B+' if sc>=700 else 'B' if sc>=650 else 'C' if sc>=600 else 'F',
        'decision': 'APPROVED' if sc>=620 else 'MANUAL_REVIEW' if sc>=600 else 'DENIED',
        'risk_level': 'low' if sc>=720 else 'medium' if sc>=620 else 'high',
        'default_probability': round(1/(1+math.exp(0.02*(sc-580))), 4)
    }

def handler(request):
    try:
        body = json.loads(request.body)
        profiles = body.get('profiles', [])
        if not profiles:
            return {'statusCode': 400, 'body': json.dumps({'error': 'profiles array required'})}
        results = [{'index': i, **score_one(p)} for i, p in enumerate(profiles)]
        approved = sum(1 for r in results if r['decision'] == 'APPROVED')
        avg = round(sum(r['credit_score'] for r in results) / len(results), 1)
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'total': len(results), 'average_score': avg,
                'approval_rate': round(approved/len(results)*100, 1),
                'summary': {'approved': approved, 'denied': len(results)-approved},
                'results': results
            })
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
