
CREATE TABLE usuarios (
	id INTEGER NOT NULL, 
	username VARCHAR, 
	email VARCHAR, 
	hashed_password VARCHAR, 
	is_admin BOOLEAN, 
	created_at DATETIME, 
	PRIMARY KEY (id)
)

;


CREATE TABLE conversaciones (
	id VARCHAR NOT NULL, 
	user_id INTEGER, 
	title VARCHAR, 
	started_at DATETIME, 
	last_updated DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES usuarios (id)
)

;


CREATE TABLE mensajes (
	id INTEGER NOT NULL, 
	conversation_id VARCHAR, 
	sender VARCHAR, 
	text TEXT, 
	timestamp DATETIME, 
	intent VARCHAR, 
	confidence FLOAT, 
	related_docs JSON, 
	PRIMARY KEY (id), 
	FOREIGN KEY(conversation_id) REFERENCES conversaciones (id)
)

;


CREATE TABLE conocimiento (
	id INTEGER NOT NULL, 
	category VARCHAR, 
	question TEXT, 
	answer TEXT, 
	is_active BOOLEAN, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id)
)

;


CREATE TABLE intenciones (
	id INTEGER NOT NULL, 
	name VARCHAR, 
	description TEXT, 
	examples JSON, 
	PRIMARY KEY (id)
)

;


CREATE TABLE entrenamiento (
	id INTEGER NOT NULL, 
	version VARCHAR, 
	status VARCHAR, 
	metrics JSON, 
	started_at DATETIME, 
	completed_at DATETIME, 
	PRIMARY KEY (id)
)

;


CREATE TABLE metricas (
	id INTEGER NOT NULL, 
	metric_type VARCHAR, 
	value FLOAT, 
	timestamp DATETIME, 
	PRIMARY KEY (id)
)

;

