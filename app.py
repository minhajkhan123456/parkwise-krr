"""Local single-user teaching server. Python standard library only."""
from http.server import HTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import json
from copy import deepcopy
from engine import initial,evaluate,commit,cancel,reallocate
STATE=initial()
class Handler(BaseHTTPRequestHandler):
    def reply(self,obj,status=200):
        raw=json.dumps(obj).encode(); self.send_response(status); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        if self.path=='/api/state': return self.reply(STATE)
        if self.path not in ('/','/index.html'): self.send_error(404); return
        raw=Path(__file__).with_name('index.html').read_bytes(); self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(raw)
    def do_POST(self):
        global STATE
        try:
            data=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))))
            if self.path=='/api/reset': STATE=initial(); return self.reply({'state':STATE})
            if self.path=='/api/cancel': cancel(STATE,data['id']); return self.reply({'state':STATE})
            if self.path=='/api/reallocate':
                result=reallocate(STATE,data['id']); return self.reply({'state':STATE,'result':result})
            if self.path=='/api/toggle':
                for b in STATE['bays']:
                    if b['id']==data['id']: b['open']=not b['open']
                return self.reply({'state':STATE})
            if self.path not in ('/api/evaluate','/api/commit'): return self.reply({'error':'Unknown action'},404)
            trial={**deepcopy(STATE),'request':data['request']}
            result=commit(trial) if self.path=='/api/commit' else evaluate(trial)
            STATE=trial; self.reply({'state':STATE,'result':result})
        except (ValueError,KeyError,TypeError) as exc: self.reply({'error':str(exc)},400)
    def log_message(self,*args): pass
if __name__=='__main__':
    print('ParkWise ready: http://127.0.0.1:8765 (Ctrl+C to stop)')
    HTTPServer(('127.0.0.1',8765),Handler).serve_forever()
