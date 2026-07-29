import os
from pathlib import Path
BASE_DIR=Path(__file__).resolve().parents[1]
DATABASE_PATH=Path(os.getenv("PROMPTOPS_DB",BASE_DIR/"promptops_studio.db"))
LLM_ENABLED=os.getenv("LLM_ENABLED","false").lower()=="true"
