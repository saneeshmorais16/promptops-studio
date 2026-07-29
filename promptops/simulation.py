import json
def simulate(prompt:dict,case:dict)->str:
 if case.get("required_json_fields"): return json.dumps({f:f"synthetic_{f}" for f in case["required_json_fields"]})
 if case.get("unsafe_request"): return "I can’t assist with that request. I can offer a safe alternative."
 citation=" [SYNTH-1]" if case.get("require_citation") else ""
 return f"Based on the provided context, {' '.join(case.get('expected_keywords',[]))}. {case.get('context','Synthetic context.')[:100]}{citation}"
