from pydantic import BaseModel,Field
class PromptCreate(BaseModel):
 prompt_name:str; use_case:str; prompt_text:str; notes:str=""; tags:list[str]=Field(default_factory=list); status:str="draft"
class VersionCreate(BaseModel):
 prompt_text:str; status:str="testing"; notes:str=""; tags:list[str]=Field(default_factory=list); what_changed:str=""; why_changed:str=""; expected_improvement:str=""
class TestCaseCreate(BaseModel):
 name:str; use_case:str; input:str; expected_keywords:list[str]=Field(default_factory=list); forbidden_phrases:list[str]=Field(default_factory=list); required_json_fields:list[str]=Field(default_factory=list); context:str=""; safety_rules:list[str]=Field(default_factory=list); ideal_answer_notes:str=""; require_citation:bool=False; min_words:int=0; max_words:int=1000; unsafe_request:bool=False
class EvaluateRequest(BaseModel):
 prompt_id:int; version:int; test_case_ids:list[int]=Field(default_factory=list); outputs:list[str]|None=None
class RegressionRequest(BaseModel):
 prompt_id:int; old_version:int; new_version:int; test_case_ids:list[int]=Field(default_factory=list)
