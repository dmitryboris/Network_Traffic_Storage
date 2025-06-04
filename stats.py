import os
from config import PCAP_PATH, ARCHIVE_PATH
from db import get_table_size


def print_stats():
    pcap_size = os.path.getsize(PCAP_PATH)
    archive_size = os.path.getsize(ARCHIVE_PATH)
    clickhouse_size = get_table_size()

    print(f"PCAP File Size: {pcap_size / 1024 / 1024:.2f} MB")
    print(f"TAR File Size: {archive_size / 1024 / 1024:.2f} MB")
    print(f"ClickHouse Table Size: {clickhouse_size / 1024 / 1024:.2f} MB")
