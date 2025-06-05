import time
from archiver import compile_pcaps


ip = '10.30.133.16'


def main():
    start_time = time.time()
    compile_pcaps(dst_ip=ip)
    print(f"Деархивация завершена за {time.time() - start_time:.2f} секунд.")


if __name__ == '__main__':
    main()
