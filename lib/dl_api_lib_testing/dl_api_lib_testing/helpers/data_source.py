from dl_core_testing.database import DbTable
from dl_core_testing.dataset import get_created_from


def data_source_settings_from_table(table: DbTable):  # type: ignore  # 2024-01-29 # TODO: Function is missing a return type annotation  [no-untyped-def]
    source_type = get_created_from(db=table.db)
    data = {  # this still requires connection_id to be defined
        "source_type": source_type,
        "parameters": {
            "table_name": table.name,
            # FIXME: learn to include or exclude it by looking at the db type
            "db_name": table.db.name,
        },
    }

    if table.schema:
        data["parameters"]["schema_name"] = table.schema  # type: ignore  # 2024-01-29 # TODO: Unsupported target for indexed assignment ("object")  [index]

    return data
