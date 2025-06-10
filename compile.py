import time
from archiver import compile_pcaps


dst_ip = '10.30.133.16'
dst_mac = 'f4:1d:6b:87:64:e7'


def main():
    start_time = time.time()
    compile_pcaps(dst_mac=dst_mac)
    print(f"Деархивация завершена за {time.time() - start_time:.2f} секунд.")


if __name__ == '__main__':
    main()
