from promptops.regression import compare
def row(score,flags=[],formatting=True):return {"overall_score":score,"safety_flags":flags,"formatting_compliance":formatting}
def test_regression_comparison():
 r=compare([row(.5)],[row(.9)]); assert r["score_change"]==.4 and r["recommendation"]=="approve"
def test_safety_regression_rejects():assert compare([row(.8)],[row(.9,["flag"])])["recommendation"]=="reject"
