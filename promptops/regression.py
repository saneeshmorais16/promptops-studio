def compare(old:list[dict],new:list[dict])->dict:
 a=sum(x["overall_score"] for x in old)/max(len(old),1); b=sum(x["overall_score"] for x in new)/max(len(new),1)
 improved=[i for i,(x,y) in enumerate(zip(old,new),1) if y["overall_score"]>x["overall_score"]]; regressed=[i for i,(x,y) in enumerate(zip(old,new),1) if y["overall_score"]<x["overall_score"]]
 safety=[i for i,(x,y) in enumerate(zip(old,new),1) if len(y["safety_flags"])>len(x["safety_flags"])]; broken=[i for i,(x,y) in enumerate(zip(old,new),1) if x["formatting_compliance"] and not y["formatting_compliance"]]
 delta=round(b-a,3); rec="reject" if safety or delta<-.1 else "needs_review" if regressed or broken else "approve"
 return {"old_score":round(a,3),"new_score":round(b,3),"score_change":delta,"improved_cases":improved,"regressed_cases":regressed,"broken_formatting":broken,"safety_regressions":safety,"recommendation":rec}
