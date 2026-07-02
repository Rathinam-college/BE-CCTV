import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection

sql_commands = """
CREATE TABLE IF NOT EXISTS "maintenance_generalbillingdocument" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL,
    "file" varchar(100) NOT NULL,
    "uploaded_at" timestamp with time zone NOT NULL,
    "general_billing_id" bigint NOT NULL REFERENCES "maintenance_generalbillinginfo" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS "maintenance_projectbillingrecord" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "record_type" varchar(10) NOT NULL,
    "number" varchar(255) NOT NULL,
    "amount" varchar(255) NULL,
    "file" varchar(100) NULL,
    "uploaded_at" timestamp with time zone NOT NULL,
    "project_id" bigint NOT NULL REFERENCES "maintenance_project" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE IF NOT EXISTS "maintenance_ticketbillingrecord" (
    "id" bigserial NOT NULL PRIMARY KEY,
    "record_type" varchar(10) NOT NULL,
    "number" varchar(255) NOT NULL,
    "amount" varchar(255) NULL,
    "file" varchar(100) NULL,
    "uploaded_at" timestamp with time zone NOT NULL,
    "ticket_id" bigint NOT NULL REFERENCES "maintenance_ticket" ("id") DEFERRABLE INITIALLY DEFERRED
);
"""

try:
    with connection.cursor() as cursor:
        cursor.execute(sql_commands)
    print("Successfully created the missing billing document tables in the database!")
except Exception as e:
    print(f"Error creating tables: {e}")
