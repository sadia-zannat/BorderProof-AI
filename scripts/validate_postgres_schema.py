"""Compile PostgreSQL DDL without claiming an actual PostgreSQL execution test."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'services/api'))
from app.db import Base
from app import models
from sqlalchemy.schema import CreateTable,CreateIndex
from sqlalchemy.dialects import postgresql
if __name__=='__main__':
 dialect=postgresql.dialect()
 for table in Base.metadata.sorted_tables:
  print(str(CreateTable(table).compile(dialect=dialect))+';')
  for index in table.indexes:print(str(CreateIndex(index).compile(dialect=dialect))+';')
 print('-- DDL compilation only. Live migrations, locking, driver and concurrency are NOT VERIFIED.')
