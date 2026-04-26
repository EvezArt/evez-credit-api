from http.server import BaseHTTPRequestHandler
import json
import math

WEIGHTS = {'payment_history': 0.35, 'credit_utilization': 0.20, 'credit_age': 0.15, 'credit_mix': 0.10, 'new_inquiries': 0.05, 'dti_ratio': 0.05, 'derogatory_marks': 0.05, 'total_accounts': 0.05}

def normalize(f, v):
    fns = {'payment_history': lambda v: min(1, max(0, v/100)), 'credit_utilization': lambda v: max(0, 1-v/100), 'credit_age': lambda v: min(1, v/25), 'credit_mix': lambda v: min(1, v/5), 'new_inquiries': lambda v: max(0, 1-v/10), 'dti_ratio': lambda v: max(0, 1-v/60), 'derogatory_marks': lambda v: max(0, 1-v/5), 'total_accounts': lambda v: min(1, v/20)}
    return fns.get(f, lambda v: 0.5)(v)

def score_one(p):
    ws = sum(normalize(f, p.get(f, 0)) * w for f, w in WEIGHTS.items())
    sc = max(300, min(850, round(300 + ws * 550)))
    return {
        'credit_score': sc,
        'grade': 'A+' if sc>=800 else 'A' if sc>=750 else 'B+' if sc>=700 else 'B' if sc>=650 else 'C' if sc>=620 else 'F',
        'decision': 'APPROVED' if sc>=620 else 'MANUAL_REVIEW' if sc>=600 else 'DENIED',
        'risk_level': 'low' if sc>=720 else 'medium' if sc>=620 else 'high',
        'default_probability': round(1/(1+math.exp(0.02*(sc-580))), 4)
    }

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            raw = self.rfile.read(content_length) if content_length > 0 else b'{}'
            body = json.loads(raw)
            profiles = body.get('profiles', [])
            if not profiles:
                resp = json.dumps({'error': 'profiles array required', 'example': {'profiles': [{'payment_history': 92, 'credit_utilization': 25, 'credit_age': 10}]}})
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(resp.encode())
                return
            results = [{'index': i, **score_one(p)} for i, p in enumerate(profiles)]
            approved = sum(1 for r in results if r['decision'] == 'APPROVED')
            avg = round(sum(r['credit_score'] for r in results) / len(results), 1)
            resp = json.dumps({
                'total': len(results),
                'average_score': avg,
                'approval_rate': round(approved/len(results)*100, 1),
                'summary': {'approved': approved, 'denied': len(results)-approved},
                'results': results,
                'model': 'EVEZ-CS-v2.0',
                'compliance': {'ecoa': True, 'fcra': True, 'reg_b': True}
            })
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
        resp = json.dumps({'endpoint': '/api/batch', 'method': 'POST', 'description': 'Batch credit scoring for multiple profiles', 'example_body': {'profiles': [{'payment_history': 92, 'credit_utilization': 25, 'credit_age': 10, 'credit_mix': 4, 'new_inquiries': 1, 'dti_ratio': 28, 'derogatory_marks': 0, 'total_accounts': 12}]}})
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
