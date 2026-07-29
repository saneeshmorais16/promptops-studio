import sqlite3
from app.config import DATABASE_PATH
def connect():
 db=sqlite3.connect(DATABASE_PATH,check_same_thread=False); db.row_factory=sqlite3.Row; return db
def init_db():
 with connect() as db: db.executescript("""CREATE TABLE IF NOT EXISTS prompts(id INTEGER PRIMARY KEY,name TEXT,use_case TEXT,created_at TEXT); CREATE TABLE IF NOT EXISTS versions(id INTEGER PRIMARY KEY,prompt_id INTEGER,version INTEGER,prompt_text TEXT,status TEXT,notes TEXT,tags TEXT,change_summary TEXT,change_reason TEXT,expected_improvement TEXT,evaluation_score REAL,created_at TEXT); CREATE TABLE IF NOT EXISTS test_cases(id INTEGER PRIMARY KEY,name TEXT,use_case TEXT,spec TEXT,created_at TEXT); CREATE TABLE IF NOT EXISTS runs(id INTEGER PRIMARY KEY,kind TEXT,result TEXT,created_at TEXT);""")
def rows(q,p=()):
 with connect() as db:return [dict(r) for r in db.execute(q,p).fetchall()]
def insert(q,p):
 with connect() as db: c=db.execute(q,p); db.commit(); return c.lastrowid
