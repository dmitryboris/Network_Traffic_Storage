from config import client


def create_table():
    client.command("""
    CREATE TABLE IF NOT EXISTS packets (
        archive_path String,
        id UInt64,
        timestamp Float64,
        wirelen UInt32,
        src_mac FixedString(17),
        dst_mac FixedString(17), 
        src_ip Nullable(IPv4), 
        dst_ip Nullable(IPv4)
    )
    ENGINE = MergeTree()
    ORDER BY id
    """)


def insert_batch(batch):
    client.insert("packets", batch)


def clear_table():
    client.command("TRUNCATE TABLE packets")


def drop_table():
    client.command("DROP TABLE IF EXISTS packets")


def get_table_size():
    query = "SELECT SUM(bytes) FROM system.parts WHERE table = 'packets' AND active = 1"
    result = client.query(query)
    rows = result.result_rows
    if rows and rows[0][0] is not None:
        return rows[0][0]
    return 0


def load_next_batch(offset, batch_size):
    return client.query(f"SELECT id, timestamp, wirelen FROM packets LIMIT {batch_size} OFFSET {offset}")


def get_archive_paths_by_dst_ip(ip):
    query = f"SELECT DISTINCT archive_path FROM packets WHERE dst_ip = '{ip}'"
    result = client.query(query)
    rows = result.result_rows
    return [row[0] for row in rows]


def get_packets_by_archive_path(archive_path, dst_ip):
    archive_path = archive_path.replace("\\", "\\\\")
    query = f"SELECT id, timestamp, wirelen FROM packets WHERE archive_path = '{archive_path}' AND dst_ip = '{dst_ip}'"
    result = client.query(query)
    return {row[0]: (row[1], row[2]) for row in result.result_rows}
