dbdir=./DB
schema_filename=schema/schema.sql
db_empty=$(dbdir)/IGDB_empty.db
db_name=newdb.db

export-db-schema:
	sqlite3 $(db_empty) '.fullschema' > $(dbdir)/$(schema_filename)

create-db-from-schema:
	sqlite3 $(dbdir)/$(db_name) < $(dbdir)/$(schema_filename)
