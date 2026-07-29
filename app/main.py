import json
from datetime import datetime,timezone
from pathlib import Path
from fastapi import FastAPI,HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.database import init_db,insert,rows
from app.schemas import *
from promptops.evaluator import evaluate_output
from promptops.simulation import simulate
from promptops.regression import compare
app=FastAPI(title="PromptOps Studio",version="1.0.0"); STATIC=Path(__file__).parent/"static"; app.mount("/static",StaticFiles(directory=STATIC),name="static")
now=lambda:datetime.now(timezone.utc).isoformat()
@app.on_event("startup")
def startup():init_db()
@app.get("/")
def home():return FileResponse(STATIC/"index.html")
@app.get("/health")
def health():return {"status":"healthy","llm_mode":"local_simulation"}
@app.post("/prompts",status_code=201)
def create_prompt(p:PromptCreate):
 pid=insert("INSERT INTO prompts(name,use_case,created_at) VALUES(?,?,?)",(p.prompt_name,p.use_case,now())); insert("INSERT INTO versions(prompt_id,version,prompt_text,status,notes,tags,created_at) VALUES(?,?,?,?,?,?,?)",(pid,1,p.prompt_text,p.status,p.notes,json.dumps(p.tags),now())); return {"prompt_id":pid,"version":1}
@app.get("/prompts")
def list_prompts():return rows("SELECT p.*,COUNT(v.id) versions FROM prompts p LEFT JOIN versions v ON p.id=v.prompt_id GROUP BY p.id ORDER BY p.id DESC")
@app.get("/prompts/{prompt_id}")
def detail(prompt_id:int):
 p=rows("SELECT * FROM prompts WHERE id=?",(prompt_id,))
 if not p:raise HTTPException(404,"Prompt not found")
 return {**p[0],"versions":versions(prompt_id)}
@app.post("/prompts/{prompt_id}/versions",status_code=201)
def add_version(prompt_id:int,v:VersionCreate):
 if not rows("SELECT id FROM prompts WHERE id=?",(prompt_id,)):raise HTTPException(404,"Prompt not found")
 n=rows("SELECT COALESCE(MAX(version),0)+1 n FROM versions WHERE prompt_id=?",(prompt_id,))[0]["n"]; insert("INSERT INTO versions(prompt_id,version,prompt_text,status,notes,tags,change_summary,change_reason,expected_improvement,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",(prompt_id,n,v.prompt_text,v.status,v.notes,json.dumps(v.tags),v.what_changed,v.why_changed,v.expected_improvement,now())); return {"prompt_id":prompt_id,"version":n}
@app.get("/prompts/{prompt_id}/versions")
def versions(prompt_id:int):return rows("SELECT * FROM versions WHERE prompt_id=? ORDER BY version",(prompt_id,))
@app.post("/test-cases",status_code=201)
def add_case(c:TestCaseCreate):return {"test_case_id":insert("INSERT INTO test_cases(name,use_case,spec,created_at) VALUES(?,?,?,?)",(c.name,c.use_case,c.model_dump_json(),now()))}
@app.get("/test-cases")
def cases():
 out=[]
 for r in rows("SELECT * FROM test_cases ORDER BY id"):
  spec=json.loads(r.pop("spec")); out.append({**r,**spec})
 return out
def run_eval(pid,version,ids,outputs=None):
 pv=rows("SELECT v.*,p.name prompt_name FROM versions v JOIN prompts p ON p.id=v.prompt_id WHERE prompt_id=? AND version=?",(pid,version))
 if not pv:raise HTTPException(404,"Prompt version not found")
 selected=[c for c in cases() if not ids or c["id"] in ids]; results=[]
 for i,c in enumerate(selected):
  output=outputs[i] if outputs and i<len(outputs) else simulate(pv[0],c); results.append({"test_case_id":c["id"],"name":c["name"],"output":output,**evaluate_output(output,c)})
 return {"prompt_name":pv[0]["prompt_name"],"version":f"v{version}","overall_score":round(sum(r["overall_score"] for r in results)/max(len(results),1),3),"cases":results,"human_review_required":True}
@app.post("/runs/evaluate")
def evaluate(req:EvaluateRequest):
 result=run_eval(req.prompt_id,req.version,req.test_case_ids,req.outputs); rid=insert("INSERT INTO runs(kind,result,created_at) VALUES(?,?,?)",("evaluation",json.dumps(result),now())); return {"run_id":rid,**result}
@app.post("/runs/regression")
def regression(req:RegressionRequest):
 old=run_eval(req.prompt_id,req.old_version,req.test_case_ids); new=run_eval(req.prompt_id,req.new_version,req.test_case_ids); result={"old_version":old["version"],"new_version":new["version"],**compare(old["cases"],new["cases"]),"human_review_required":True}; rid=insert("INSERT INTO runs(kind,result,created_at) VALUES(?,?,?)",("regression",json.dumps(result),now())); return {"run_id":rid,**result}
@app.get("/runs")
def all_runs():return [{**r,"result":json.loads(r["result"])} for r in rows("SELECT * FROM runs ORDER BY id DESC")]
@app.get("/runs/{run_id}")
def get_run(run_id:int):
 r=rows("SELECT * FROM runs WHERE id=?",(run_id,))
 if not r:raise HTTPException(404,"Run not found")
 return {**r[0],"result":json.loads(r[0]["result"])}
@app.get("/dashboard")
def dashboard():
 ps=rows("SELECT COUNT(*) n FROM prompts")[0]["n"]; vs=rows("SELECT status,COUNT(*) n FROM versions GROUP BY status"); rs=all_runs(); ev=[x["result"]["overall_score"] for x in rs if x["kind"]=="evaluation"]; cs=[c for x in rs if x["kind"]=="evaluation" for c in x["result"]["cases"]]
 return {"total_prompts":ps,"approved_prompts":sum(x["n"] for x in vs if x["status"]=="approved"),"draft_prompts":sum(x["n"] for x in vs if x["status"]=="draft"),"average_evaluation_score":round(sum(ev)/max(len(ev),1),3),"regressions_detected":sum(len(x["result"].get("regressed_cases",[])) for x in rs if x["kind"]=="regression"),"safety_flags":sum(len(c["safety_flags"]) for c in cs),"formatting_failures":sum(not c["formatting_compliance"] for c in cs)}
