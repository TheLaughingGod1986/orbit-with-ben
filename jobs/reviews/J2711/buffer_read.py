import json,pathlib
from audit_tags import OWB,envfile,req
E=envfile(OWB/'07_Content-Ops/.env')
def gql(q,variables=None):
 data=json.dumps(dict(query=q,variables=variables or {})).encode()
 import urllib.request
 r=urllib.request.Request('https://api.buffer.com',data=data,headers={'Authorization':'Bearer '+E['BUFFER_API_KEY'],'Content-Type':'application/json'})
 return json.load(urllib.request.urlopen(r,timeout=35))
if __name__=='__main__':
 ledger=json.loads((OWB/'00_Brand/Channel-Setup/social/BUFFER_POSTS.json').read_text())['videos']
 out={}
 for network,p in ledger['uhZSRcvngvE']['channels'].items():
  out[network]=gql('query($input:PostInput!){post(input:$input){id status text}}',{'input':{'id':p['postId']}})
 print(json.dumps(out,indent=2));pathlib.Path(__file__).with_name('mars_buffer_posts.json').write_text(json.dumps(out,indent=2)+'\n')
 schema=gql('{__type(name:"Post"){fields{name type{kind name ofType{kind name}}}}}')
 pathlib.Path(__file__).with_name('buffer_post_schema.json').write_text(json.dumps(schema,indent=2)+'\n')
 print(json.dumps(schema))
