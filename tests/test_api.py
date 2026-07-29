def test_health(client):assert client.get('/health').json()["status"]=="healthy"
def test_full_workflow(client):
 p=client.post('/prompts',json={"prompt_name":"Synthetic RAG","use_case":"rag","prompt_text":"Use context"}); assert p.status_code==201; pid=p.json()["prompt_id"]
 assert client.post(f'/prompts/{pid}/versions',json={"prompt_text":"Use context and cite"}).json()["version"]==2
 assert client.post('/test-cases',json={"name":"Grounding","use_case":"rag","input":"Synthetic question","context":"alpha policy","expected_keywords":["alpha"],"require_citation":True}).status_code==201
 assert client.post('/runs/evaluate',json={"prompt_id":pid,"version":2}).json()["overall_score"]>0
 assert client.get('/dashboard').json()["total_prompts"]==1
def test_invalid_version(client):assert client.post('/runs/evaluate',json={"prompt_id":99,"version":1}).status_code==404
