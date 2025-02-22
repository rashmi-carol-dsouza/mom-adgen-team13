# Connection Test

This script is used to test the connection with an instance of the [koyeb db](https://www.koyeb.com/docs/databases) called `mom-2025-team13-db`.

## Pre-requisites

To run this script you need to create a `.env` file in the same directory as this `README.md`.

The contents of the `.env` should be as follows:

```
DATABASE_HOST=ep-aged-forest-a2sd5mrk.eu-central-1.pg.koyeb.app
DATABASE_USER=koyeb-adm
DATABASE_PASSWORD=ASK_LARRY_IN_CHAT
DATABASE_NAME=koyebdb
SAMPLE_DATA_PATH = "db/scripts/connection_test/sample-data.csv"
MIGRATIONS_PATH = "db/migrations/V1__create_initial_schema.sql"
FLAG_INIT_DB=DISABLED
```

## Running

Navigate to the `bff-api` directory, execute `make test-connection`.
