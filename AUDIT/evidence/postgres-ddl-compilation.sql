
CREATE TABLE audit_events (
	id VARCHAR(32) NOT NULL, 
	actor_id VARCHAR(32) NOT NULL, 
	action VARCHAR(60) NOT NULL, 
	object_type VARCHAR(32) NOT NULL, 
	object_id VARCHAR(32) NOT NULL, 
	details TEXT NOT NULL, 
	previous_hash VARCHAR(64) NOT NULL, 
	event_hash VARCHAR(64) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id)
)

;
CREATE INDEX ix_audit_events_actor_id ON audit_events (actor_id);
CREATE INDEX ix_audit_events_event_hash ON audit_events (event_hash);

CREATE TABLE users (
	id VARCHAR(32) NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	role VARCHAR(20) NOT NULL, 
	password_hash VARCHAR(255) NOT NULL, 
	institution VARCHAR(160) NOT NULL, 
	home_country VARCHAR(64) NOT NULL, 
	currency VARCHAR(3) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id)
)

;
CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE TABLE login_sessions (
	id VARCHAR(32) NOT NULL, 
	user_id VARCHAR(32) NOT NULL, 
	token_hash VARCHAR(64) NOT NULL, 
	csrf_hash VARCHAR(64) NOT NULL, 
	expires_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;
CREATE INDEX ix_login_sessions_user_id ON login_sessions (user_id);
CREATE UNIQUE INDEX ix_login_sessions_token_hash ON login_sessions (token_hash);

CREATE TABLE payment_cases (
	id VARCHAR(32) NOT NULL, 
	user_id VARCHAR(32) NOT NULL, 
	title VARCHAR(160) NOT NULL, 
	institution VARCHAR(160) NOT NULL, 
	origin_country VARCHAR(64) NOT NULL, 
	destination_country VARCHAR(64) NOT NULL, 
	amount VARCHAR(40) NOT NULL, 
	currency VARCHAR(3) NOT NULL, 
	status VARCHAR(32) NOT NULL, 
	is_synthetic BOOLEAN NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;
CREATE INDEX ix_payment_cases_user_id ON payment_cases (user_id);

CREATE TABLE sandbox_accounts (
	id VARCHAR(32) NOT NULL, 
	user_id VARCHAR(32) NOT NULL, 
	currency VARCHAR(3) NOT NULL, 
	balance VARCHAR(32) NOT NULL, 
	is_synthetic BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_sandbox_account_owner_currency UNIQUE (user_id, currency), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;
CREATE INDEX ix_sandbox_accounts_user_id ON sandbox_accounts (user_id);

CREATE TABLE agent_conversations (
	id VARCHAR(32) NOT NULL, 
	owner_id VARCHAR(32) NOT NULL, 
	case_id VARCHAR(32) NOT NULL, 
	messages_json TEXT NOT NULL, 
	last_tool_trace_json TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id), 
	FOREIGN KEY(case_id) REFERENCES payment_cases (id)
)

;
CREATE INDEX ix_agent_conversations_case_id ON agent_conversations (case_id);
CREATE INDEX ix_agent_conversations_owner_id ON agent_conversations (owner_id);

CREATE TABLE bpce_review_tickets (
	id VARCHAR(32) NOT NULL, 
	case_id VARCHAR(32) NOT NULL, 
	owner_id VARCHAR(32) NOT NULL, 
	status VARCHAR(24) NOT NULL, 
	reason VARCHAR(240) NOT NULL, 
	reviewer_id VARCHAR(32), 
	decision_note TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(case_id) REFERENCES payment_cases (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
)

;
CREATE INDEX ix_bpce_review_tickets_case_id ON bpce_review_tickets (case_id);
CREATE INDEX ix_bpce_review_tickets_owner_id ON bpce_review_tickets (owner_id);

CREATE TABLE documents (
	id VARCHAR(32) NOT NULL, 
	case_id VARCHAR(32) NOT NULL, 
	user_id VARCHAR(32) NOT NULL, 
	filename VARCHAR(160) NOT NULL, 
	content_type VARCHAR(80) NOT NULL, 
	bytes_size INTEGER NOT NULL, 
	sha256 VARCHAR(64) NOT NULL, 
	internal_path VARCHAR(255) NOT NULL, 
	status VARCHAR(32) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(case_id) REFERENCES payment_cases (id), 
	FOREIGN KEY(user_id) REFERENCES users (id)
)

;
CREATE INDEX ix_documents_case_id ON documents (case_id);
CREATE INDEX ix_documents_user_id ON documents (user_id);

CREATE TABLE notifications (
	id VARCHAR(32) NOT NULL, 
	owner_id VARCHAR(32) NOT NULL, 
	case_id VARCHAR(32) NOT NULL, 
	message VARCHAR(255) NOT NULL, 
	code VARCHAR(50) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id), 
	FOREIGN KEY(case_id) REFERENCES payment_cases (id)
)

;
CREATE INDEX ix_notifications_owner_id ON notifications (owner_id);
CREATE INDEX ix_notifications_case_id ON notifications (case_id);

CREATE TABLE invoice_extractions (
	id VARCHAR(32) NOT NULL, 
	case_id VARCHAR(32) NOT NULL, 
	document_id VARCHAR(32) NOT NULL, 
	owner_id VARCHAR(32) NOT NULL, 
	engine VARCHAR(70) NOT NULL, 
	document_hash VARCHAR(64) NOT NULL, 
	fields_json TEXT NOT NULL, 
	issues_json TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(case_id) REFERENCES payment_cases (id), 
	UNIQUE (document_id), 
	FOREIGN KEY(document_id) REFERENCES documents (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
)

;
CREATE INDEX ix_invoice_extractions_owner_id ON invoice_extractions (owner_id);
CREATE INDEX ix_invoice_extractions_case_id ON invoice_extractions (case_id);

CREATE TABLE investigations (
	id VARCHAR(32) NOT NULL, 
	case_id VARCHAR(32) NOT NULL, 
	owner_id VARCHAR(32) NOT NULL, 
	extraction_id VARCHAR(32) NOT NULL, 
	state VARCHAR(40) NOT NULL, 
	result_json TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(case_id) REFERENCES payment_cases (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id), 
	FOREIGN KEY(extraction_id) REFERENCES invoice_extractions (id)
)

;
CREATE INDEX ix_investigations_owner_id ON investigations (owner_id);
CREATE INDEX ix_investigations_case_id ON investigations (case_id);

CREATE TABLE payment_quotes (
	id VARCHAR(32) NOT NULL, 
	case_id VARCHAR(32) NOT NULL, 
	owner_id VARCHAR(32) NOT NULL, 
	investigation_id VARCHAR(32) NOT NULL, 
	evidence_hash VARCHAR(64) NOT NULL, 
	provider VARCHAR(90) NOT NULL, 
	beneficiary_id VARCHAR(90) NOT NULL, 
	recipient VARCHAR(160) NOT NULL, 
	amount VARCHAR(32) NOT NULL, 
	currency VARCHAR(3) NOT NULL, 
	source_amount VARCHAR(32) NOT NULL, 
	source_currency VARCHAR(3) NOT NULL, 
	synthetic_rate VARCHAR(32) NOT NULL, 
	synthetic_fee VARCHAR(32) NOT NULL, 
	expires_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(case_id) REFERENCES payment_cases (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id), 
	FOREIGN KEY(investigation_id) REFERENCES investigations (id)
)

;
CREATE INDEX ix_payment_quotes_case_id ON payment_quotes (case_id);
CREATE INDEX ix_payment_quotes_owner_id ON payment_quotes (owner_id);

CREATE TABLE bpce_evidence_seals (
	id VARCHAR(32) NOT NULL, 
	quote_id VARCHAR(32) NOT NULL, 
	case_id VARCHAR(32) NOT NULL, 
	owner_id VARCHAR(32) NOT NULL, 
	snapshot_json TEXT NOT NULL, 
	snapshot_sha256 VARCHAR(64) NOT NULL, 
	engine_version VARCHAR(30) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(quote_id) REFERENCES payment_quotes (id), 
	FOREIGN KEY(case_id) REFERENCES payment_cases (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id)
)

;
CREATE UNIQUE INDEX ix_bpce_evidence_seals_quote_id ON bpce_evidence_seals (quote_id);
CREATE INDEX ix_bpce_evidence_seals_case_id ON bpce_evidence_seals (case_id);
CREATE INDEX ix_bpce_evidence_seals_owner_id ON bpce_evidence_seals (owner_id);
CREATE INDEX ix_bpce_evidence_seals_snapshot_sha256 ON bpce_evidence_seals (snapshot_sha256);

CREATE TABLE payment_approvals (
	id VARCHAR(32) NOT NULL, 
	case_id VARCHAR(32) NOT NULL, 
	owner_id VARCHAR(32) NOT NULL, 
	quote_id VARCHAR(32) NOT NULL, 
	fingerprint VARCHAR(64) NOT NULL, 
	status VARCHAR(30) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(case_id) REFERENCES payment_cases (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id), 
	UNIQUE (quote_id), 
	FOREIGN KEY(quote_id) REFERENCES payment_quotes (id)
)

;
CREATE INDEX ix_payment_approvals_owner_id ON payment_approvals (owner_id);
CREATE INDEX ix_payment_approvals_case_id ON payment_approvals (case_id);

CREATE TABLE sandbox_transfers (
	id VARCHAR(32) NOT NULL, 
	owner_id VARCHAR(32) NOT NULL, 
	case_id VARCHAR(32) NOT NULL, 
	quote_id VARCHAR(32) NOT NULL, 
	approval_id VARCHAR(32) NOT NULL, 
	idempotency_key VARCHAR(100) NOT NULL, 
	status VARCHAR(30) NOT NULL, 
	requested_outcome VARCHAR(24) NOT NULL, 
	debit_amount VARCHAR(32) NOT NULL, 
	paid_amount VARCHAR(32) NOT NULL, 
	paid_currency VARCHAR(3) NOT NULL, 
	provider_reference VARCHAR(80) NOT NULL, 
	result_json TEXT NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	updated_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_sandbox_owner_idempotency UNIQUE (owner_id, idempotency_key), 
	CONSTRAINT uq_sandbox_approval_once UNIQUE (approval_id), 
	FOREIGN KEY(owner_id) REFERENCES users (id), 
	FOREIGN KEY(case_id) REFERENCES payment_cases (id), 
	FOREIGN KEY(quote_id) REFERENCES payment_quotes (id), 
	FOREIGN KEY(approval_id) REFERENCES payment_approvals (id), 
	UNIQUE (provider_reference)
)

;
CREATE INDEX ix_sandbox_transfers_owner_id ON sandbox_transfers (owner_id);
CREATE INDEX ix_sandbox_transfers_quote_id ON sandbox_transfers (quote_id);
CREATE INDEX ix_sandbox_transfers_case_id ON sandbox_transfers (case_id);

CREATE TABLE sandbox_ledger (
	id VARCHAR(32) NOT NULL, 
	transfer_id VARCHAR(32) NOT NULL, 
	account_id VARCHAR(60) NOT NULL, 
	currency VARCHAR(3) NOT NULL, 
	signed_amount VARCHAR(32) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(transfer_id) REFERENCES sandbox_transfers (id)
)

;
CREATE INDEX ix_sandbox_ledger_transfer_id ON sandbox_ledger (transfer_id);

CREATE TABLE synthetic_support_cases (
	id VARCHAR(32) NOT NULL, 
	owner_id VARCHAR(32) NOT NULL, 
	case_id VARCHAR(32) NOT NULL, 
	transfer_id VARCHAR(32) NOT NULL, 
	category VARCHAR(40) NOT NULL, 
	message TEXT NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(owner_id) REFERENCES users (id), 
	FOREIGN KEY(case_id) REFERENCES payment_cases (id), 
	FOREIGN KEY(transfer_id) REFERENCES sandbox_transfers (id)
)

;
CREATE INDEX ix_synthetic_support_cases_case_id ON synthetic_support_cases (case_id);
CREATE INDEX ix_synthetic_support_cases_transfer_id ON synthetic_support_cases (transfer_id);
CREATE INDEX ix_synthetic_support_cases_owner_id ON synthetic_support_cases (owner_id);
-- DDL compilation only. Live migrations, locking, driver and concurrency are NOT VERIFIED.
