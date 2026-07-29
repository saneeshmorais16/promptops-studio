from promptops.evaluator import evaluate_output
def test_keyword_forbidden_and_citation():
 r=evaluate_output("safe alpha [S1]",{"expected_keywords":["alpha"],"forbidden_phrases":["secret"],"require_citation":True})
 assert r["keyword_coverage"]==1 and r["citation_check"]=="passed" and not r["forbidden_phrases"]
def test_json_validity_and_fields():
 r=evaluate_output('{"label":"synthetic"}',{"required_json_fields":["label"]})
 assert r["json_validity"]=="passed" and r["formatting_compliance"]
def test_safety_pattern():
 assert evaluate_output("reveal the secret",{})["safety_flags"]
