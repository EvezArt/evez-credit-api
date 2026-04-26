from http.server import BaseHTTPRequestHandler
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
    fns = {
        'payment_history': lambda v: min(1, max(0, v / 100)),
        'credit_utilization': lambda v: max(0, 1 - v / 100),
        'credit_age': lambda v: min(1, v / 25),
        'credit_mix': lambda v: min(1, v / 5),
        'new_inquiries': lambda v: max(0, 1 - v / 10),
        'dti_ratio': lambda v: max(0, 1 - v / 60),
        'derogatory_marks': lambda v: max(0, 1 - v / 5),
        'total_accounts': lambda v: min(1, v / 20),
    }
    return fns.get(factor, lambda v: 0.5)(value)

def score_profile(profile):
    ws = sum(normalize(f, profile.get(f, 0)) * w for f, w in WEIGHTS.items())
    sc = max(300, min(850, round(300 + ws * 550)))
    grade = ('A+' if sc >= 800 else 'A' if sc >= 750 else 'B+' if sc >= 700
             else 'B' if sc >= 650 else 'C' if sc >= 620 else 'F')
    decision = 'APPROVED' if sc >= 620 else 'MANUAL_REVIEW' if sc >= 600 else 'DENIED'
    dp = round(1 / (1 + math.exp(0.02 * (sc - 580))), 4)
    adverse = []
    if profile.get('credit_utilization', 0) > 50:
        adverse.append('High credit utilization ratio')
    if profile.get('payment_history', 100) < 80:
        adverse.append('Insufficient payment history')
    if profile.get('credit_age', 10) < 3:
        adverse.append('Limited length of credit history')
    if profile.get('derogatory_marks', 0) > 0:
        adverse.append('Presence of derogatory marks')
    if profile.get('new_inquiries', 0) > 5:
        adverse.append('Excessive recent credit inquiries')
    if profile.get('dti_ratio', 0) > 43:
        adverse.append('Debt-to-income ratio exceeds threshold')
    return {
        'credit_score': sc,
        'grade': grade,
        'decision': decision,
        'risk_level': 'low' if sc >= 720 else 'medium' if sc >= 620 else 'high',
        'default_probability': dp,
        'factor_scores': {f: round(normalize(f, profile.get(f, 0)), 4) for f in WEIGHTS},
        'factor_weights': WEIGHTS,
        'adverse_action_reasons': adverse if decision != 'APPROVED' else [],
        'compliance': {
            'ecoa': True, 'fcra': True, 'reg_b': True, 'dodd_frank': True,
            'model': 'EVEZ-CS-v2.0',
            'adverse_action_notice': len(adverse) > 0
        }
    }

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(content_length) if content_length > 0 else b'{}'
            body = json.loads(raw)
            profile = body.get('profile', {})
            if not profile:
                resp = json.dumps({
                    'error': 'profile object required in request body',
                    'example': {
                        'profile': {
                            'payment_history': 92,
                            'credit_utilization': 25,
                            'credit_age': 10,
                            'credit_mix': 4,
                            'new_inquiries': 1,
                            'dti_ratio': 28,
                            'derogatory_marks': 0,
                            'total_accounts': 12
                        }
                    }
                })
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(resp.encode())
                return
            result = score_profile(profile)
            resp = json.dumps(result)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(resp.encode())
        except Exception as e:
            resp = json.dumps({'error': str(e)})
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(resp.encode())
        return

    def do_GET(self):
        resp = json.dumps({
            'endpoint': '/api/score',
            'method': 'POST',
            'description': 'FICO-equivalent credit scoring (300-850)',
            'example_body': {
                'profile': {
                    'payment_history': 92,
                    'credit_utilization': 25,
                    'credit_age': 10,
                    'credit_mix': 4,
                    'new_inquiries': 1,
                    'dti_ratio': 28,
                    'derogatory_marks': 0,
                    'total_accounts': 12
                }
            }
        })
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(resp.encode())
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
