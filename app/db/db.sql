BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "transactions" (
	"transaction_id"	TEXT NOT NULL,
	"account_id"	TEXT NOT NULL,
	"date"	TEXT NOT NULL,
	"amount"	INTEGER NOT NULL,
	"description"	TEXT,
	"type"	TEXT,
	"category"	TEXT,
	"sub_category"	TEXT,
	"added"	TEXT NOT NULL,
	FOREIGN KEY("account_id") REFERENCES "accounts"("id"),
	PRIMARY KEY("transaction_id")
);
CREATE TABLE IF NOT EXISTS "accounts" (
	"id"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"balance"	INTEGER NOT NULL,
	"number"	TEXT,
	"bank"	TEXT,
	"logo"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "shares" (
	"id"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"symbol"	TEXT NOT NULL,
	"logo"	TEXT NOT NULL,
	"shares"	INTEGER NOT NULL,
	"value"	INTEGER NOT NULL,
	"returns"	INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS "kiwisavers" (
	"id"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"amount"	INTEGER NOT NULL,
	"provider_name"	TEXT,
	"provider_logo"	TEXT,
	"employer_contributions"	INTEGER,
	"personal_contributions"	INTEGER,
	"tax"	INTEGER,
	"member_tax"	INTEGER,
	"fees"	INTEGER,
	"previous_balance"	INTEGER,
	"withdrawals"	INTEGER,
	"date"	TEXT
);
CREATE TABLE IF NOT EXISTS "kiwisavers_history" (
	"id"	TEXT,
	"name"	TEXT,
	"amount"	INT,
	"provider_name"	TEXT,
	"provider_logo"	TEXT,
	"employer_contributions"	INT,
	"personal_contributions"	INT,
	"tax"	INT,
	"member_tax"	INT,
	"fees"	INT,
	"previous_balance"	INT,
	"withdrawals"	INT,
	"date"	TEXT
);
CREATE TRIGGER move_to_history_trigger
BEFORE DELETE ON kiwisavers
BEGIN
    INSERT INTO kiwisavers_history SELECT * FROM kiwisavers;
END;
COMMIT;
