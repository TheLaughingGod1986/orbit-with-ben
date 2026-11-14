"""Let Buffer reparse the preserved URL after its Facebook annotation-input coercion."""
import json,pathlib,time
from buffer_read import gql
from repair_scheduled import FIELDS
ID='6af5652a97798e85b9ebc183'
q='query($input:PostInput!){post(input:$input){'+FIELDS+'}}'
before=gql(q,{'input':{'id':ID}})['data']['post']
assert before['status']=='scheduled' and before['dueAt']=='2026-11-18T11:30:00.000Z'
a=before['assets'][0]
payload={'id':ID,'text':before['text'],'assets':[{'video':{'url':a['source'],'metadata':{k:v for k,v in a['video'].items() if v is not None}}}],'metadata':{'facebook':{'type':before['metadata']['type'],'firstComment':before['metadata']['firstComment'],'annotations':[]}}}
mutation=gql('mutation($input:EditPostInput!){editPost(input:$input){__typename ... on PostActionSuccess{post{id text status dueAt}} ... on MutationError{message}}}',{'input':payload})
assert mutation['data']['editPost']['__typename']=='PostActionSuccess',mutation
for i in range(5):
 after=gql(q,{'input':{'id':ID}})['data']['post']
 urls=[x for x in after['metadata']['annotations'] if x['text']=='https://youtu.be/c5AdqQsnnys']
 if urls and urls[0]['type']=='url':break
 time.sleep(1)
assert urls and urls[0]['type']=='url', after['metadata']
assert {k:v for k,v in before.items() if k!='metadata'}=={k:v for k,v in after.items() if k!='metadata'}
pathlib.Path(__file__).with_name('facebook_final_annotation.json').write_text(json.dumps(dict(before=before,mutation=mutation,after=after),indent=2)+'\n')
print('Facebook URL parsed as URL; text, status, dueAt and video unchanged')
