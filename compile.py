import time
from archiver import compile_pcap


def main():
    start_time = time.time()
    compile_pcap()
    print(f"Архивация завершена за {time.time() - start_time:.2f} секунд.")


if __name__ == '__main__':
    main()
