import clickhouse_connect

PCAP_PATH = r'C:\Users\...\pcap.pcap'
ARCHIVE_PATH = r'C:\Users\...\pcap.tar.zst'
RESTORED_PCAP_PATH = r'C:\Users\...\copy_pcap.pcap'
BATCH_SIZE = 5000

client = clickhouse_connect.get_client(
    host='localhost',
    port=8123,
    username='default',
    password='',
    database='default',
)
