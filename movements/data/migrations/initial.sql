CREATE TABLE "movements" (
	"id"	INTEGER,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"from_currency"	INTEGER NOT NULL,
	"from_quantity"	REAL NOT NULL,
	"to_currency"	INTEGER NOT NULL,
	"to_quantity"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)