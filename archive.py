import time
from db import drop_table, create_table
from archiver import process_pcap
from stats import print_stats


def main():
    start_time = time.time()
    drop_table()
    create_table()
    process_pcap()
    print_stats()
    print(f"Архивация завершена за {time.time() - start_time:.2f} секунд.")


if __name__ == '__main__':
    main()
