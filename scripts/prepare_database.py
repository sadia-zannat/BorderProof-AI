"""Additive schema initialization/index migration for the configured database.
Back up the database and uploads before running against existing data.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'services/api'))
from app.db import init_schema,engine
if __name__=='__main__':
 init_schema()
 print('Schema initialized/rechecked for dialect:',engine.dialect.name)
 print('Existing rows retained. Duplicate financial rows cause an explicit migration failure.')
