import clickhouse_connect

PCAP_PATH = r'C:\Users\Dima\Downloads\new\part1.pcap'
ARCHIVE_PATH = r'C:\Users\Dima\Downloads\new\part1.tar.zst'
RESTORED_PCAP_PATH = r'C:\Users\Dima\Downloads\new\COPY.pcap'
BATCH_SIZE = 5000

client = clickhouse_connect.get_client(
    host='localhost',
    port=8123,
    username='default',
    password='',
    database='default',
)
# client = Client(
#     host='localhost',
#     port=9000,
#     user='default',
#     password='',
#     database='default'
# )
