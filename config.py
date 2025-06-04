from clickhouse_driver import Client

PCAP_PATH = r''
ARCHIVE_PATH = r''
RESTORED_PCAP_PATH = r''
BATCH_SIZE = 5000

client = Client(
    host='localhost',
    port=9000,
    user='default',
    password='',
    database='default'
)
