import os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
os.environ["PROMPTOPS_DB"]="test_promptops.db"
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db,connect
@pytest.fixture(autouse=True)
def clean_db():
 init_db()
 with connect() as db:
  for t in ("runs","test_cases","versions","prompts"):db.execute(f"DELETE FROM {t}")
  db.commit()
@pytest.fixture
def client():return TestClient(app)
