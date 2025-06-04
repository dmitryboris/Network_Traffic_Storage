from config import client


def create_table():
    client.execute("""
    CREATE TABLE IF NOT EXISTS packets (
        id UInt64,
        timestamp Float64,
        wirelen UInt32
    )
    ENGINE = MergeTree()
    ORDER BY id
    """)


def insert_batch(batch):
    client.execute("INSERT INTO packets VALUES", batch)


def clear_table():
    client.execute("TRUNCATE TABLE packets")


def drop_table():
    client.execute("DROP TABLE IF EXISTS packets")


def get_table_size():
    query = "SELECT SUM(bytes) FROM system.parts WHERE table = 'packets' AND active = 1"
    result = client.execute(query)
    return result[0][0] if result[0][0] else 0


def load_next_batch(offset, batch_size):
    return client.execute(f"SELECT id, timestamp, wirelen FROM packets LIMIT {batch_size} OFFSET {offset}")
