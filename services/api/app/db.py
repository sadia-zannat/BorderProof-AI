"""Database setup. SQLite locally; PostgreSQL URL usable with a compatible driver."""
from __future__ import annotations
import os
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DB = ROOT / 'runtime' / 'borderproof.sqlite3'
DEFAULT_DB.parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{DEFAULT_DB}')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {}, pool_pre_ping=True)
if DATABASE_URL.startswith('sqlite'):
    @event.listens_for(engine, 'connect')
    def _sqlite_fk(conn, _):
        cursor = conn.cursor(); cursor.execute('PRAGMA foreign_keys=ON'); cursor.close()
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
class Base(DeclarativeBase):
    pass

def db_session():
    with SessionLocal() as db:
        yield db


def init_schema():
    """Non-destructive V1→V2→V3 additive schema migration, safe to re-run."""
    from sqlalchemy import text
    from . import models as _models  # noqa: F401
    with engine.begin() as conn:
        conn.execute(text('CREATE TABLE IF NOT EXISTS schema_versions (version INTEGER PRIMARY KEY, description VARCHAR(120) NOT NULL)'))
        version = conn.execute(text('SELECT MAX(version) FROM schema_versions')).scalar()
        if version not in (None, 1, 2, 3, 4, 5, 6):
            raise RuntimeError(f'Unsupported schema version {version}')
    # Add optional routing columns without dropping any financial records.
    # Existing origin defaults to Bangladesh; target currency follows old invoice currency.
    if DATABASE_URL.startswith('sqlite'):
        with engine.begin() as conn:
            from sqlalchemy import inspect
            if inspect(conn).has_table('payment_cases'):
                columns={x['name'] for x in inspect(conn).get_columns('payment_cases')}
                if 'source_currency' not in columns:
                    conn.execute(text("ALTER TABLE payment_cases ADD COLUMN source_currency VARCHAR(3) DEFAULT 'BDT'"))
                if 'destination_currency' not in columns:
                    conn.execute(text('ALTER TABLE payment_cases ADD COLUMN destination_currency VARCHAR(3)'))
                    conn.execute(text('UPDATE payment_cases SET destination_currency = currency WHERE destination_currency IS NULL'))
    else:
        # Fresh PostgreSQL databases have no payment_cases table yet.
        # Add columns only during upgrades; create_all handles brand-new installs.
        from sqlalchemy import inspect
        if inspect(engine).has_table('payment_cases'):
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE payment_cases ADD COLUMN IF NOT EXISTS source_currency VARCHAR(3) DEFAULT 'BDT'"))
                conn.execute(text('ALTER TABLE payment_cases ADD COLUMN IF NOT EXISTS destination_currency VARCHAR(3)'))
                conn.execute(text('UPDATE payment_cases SET destination_currency = currency WHERE destination_currency IS NULL'))
    Base.metadata.create_all(engine, checkfirst=True)
    with engine.begin() as conn:
        # V5.3 additive safety indexes. Existing duplicate rows stop migration;
        # never silently delete financial history to make a unique index succeed.
        for name,table,columns in (
            ('uq_sandbox_account_owner_currency','sandbox_accounts','user_id, currency'),
            ('uq_sandbox_approval_once','sandbox_transfers','approval_id'),
            ('uq_sandbox_ledger_posting','sandbox_ledger','transfer_id, account_id')):
            conn.execute(text(f'CREATE UNIQUE INDEX IF NOT EXISTS {name} ON {table} ({columns})'))
        conn.execute(text("CREATE UNIQUE INDEX IF NOT EXISTS uq_sandbox_open_or_completed_case ON sandbox_transfers (case_id) WHERE status IN ('COMPLETED','UNKNOWN')"))
        version = conn.execute(text('SELECT MAX(version) FROM schema_versions')).scalar()
        if version is None:
            conn.execute(text('INSERT INTO schema_versions(version,description) VALUES (1, :description)'), {'description':'V1 foundation schema'})
        if version not in (2, 3, 4, 5, 6):
            conn.execute(text('INSERT INTO schema_versions(version,description) VALUES (2, :description)'), {'description':'V2 financial agent and sandbox tables'})
        if version not in (3,4,5,6):
            conn.execute(text('INSERT INTO schema_versions(version,description) VALUES (3, :description)'), {'description':'V3 evidence seals and human review queue'})
        if version not in (4, 5, 6):
            conn.execute(text('INSERT INTO schema_versions(version,description) VALUES (4, :description)'), {'description':'V5 local-only support and evidence export'})
        if version not in (5,6):
            conn.execute(text('INSERT INTO schema_versions(version,description) VALUES (5, :description)'), {'description':'V5.1 isolated read-only local LLM agent chat'})

        if version != 6:
            conn.execute(text('INSERT INTO schema_versions(version,description) VALUES (6, :description)'), {'description':'V5.4 bidirectional reference planning and evidence diagnostics; no live payments'})
