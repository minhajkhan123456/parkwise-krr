"""Optional local API smoke check: python test_http.py"""
import threading, urllib.request, json
from app import Handler, HTTPServer
server=HTTPServer(('127.0.0.1',0),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
url='http://127.0.0.1:'+str(server.server_port)
def post(path,data):
    req=urllib.request.Request(url+'/api/'+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(req))
try:
    q=json.load(urllib.request.urlopen(url+'/api/state'))['request']
    assert post('evaluate',{'request':q})['result']['recommended']=='G1'
    assert post('commit',{'request':q})['state']['bookings'][0]['bay']=='G1'
    q['id']='R2'
    assert post('evaluate',{'request':q})['result']['recommended']=='G2'
    assert post('cancel',{'id':'R1'})['state']['bookings']==[]
    assert post('toggle',{'id':'G1'})['state']['bays'][0]['open']==False
    assert post('reset',{})['state']['bays'][0]['open']==True
    assert '<!doctype html>' in urllib.request.urlopen(url).read().decode()
    print('PASS: HTTP state, HTML, evaluate, commit, cancel, closure and reset')
finally: server.shutdown()
