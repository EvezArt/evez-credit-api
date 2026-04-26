from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime, timezone

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({
            'status': 'healthy',
            'model': 'EVEZ-CS-v2.0',
            'version': '2.0.0',
            'description': 'FICO-equivalent credit scoring engine — ECOA/FCRA/Reg B compliant',
            'endpoints': {
                'POST /api/score': 'Score a single credit profile (300-850)',
                'POST /api/batch': 'Score multiple profiles in batch',
                'GET /api/health': 'System status',
                'GET /': 'This page'
            },
            'example_request': {
                'url': 'POST /api/score',
                'body': {
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
            },
            'compliance': {'ecoa': True, 'fcra': True, 'reg_b': True, 'dodd_frank': True},
            'open_source': 'https://github.com/EvezArt/evez-credit-api',
            'supabase_api': 'https://vziaqxquzohqskesuxgz.supabase.co/functions/v1/credit-score',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'platform': 'vercel'
        })
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body.encode())
        return

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        return
