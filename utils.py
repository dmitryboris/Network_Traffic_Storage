from scapy.layers.inet import IP
from scapy.layers.l2 import Ether


def get_timestamp(pkt_metadata):
    # Если есть поля sec и usec — значит это старый PacketMetadata
    if hasattr(pkt_metadata, 'sec'):
        return pkt_metadata.sec + pkt_metadata.usec / 1_000_000

    # Иначе считаем, что это PacketMetadataNG
    elif hasattr(pkt_metadata, 'tshigh'):
        timestamp_64 = (pkt_metadata.tshigh << 32) | pkt_metadata.tslow
        tsresol = getattr(pkt_metadata, 'tsresol', 6)

        if isinstance(tsresol, int) and 0 <= tsresol <= 9:
            resolution = 10 ** -tsresol
        else:
            resolution = 1e-6

        return timestamp_64 * resolution

    else:
        # Неизвестный формат — возвращаем 0
        return 0.0


def extract_mac_addresses(packet):
    src_mac = packet[Ether].src
    dst_mac = packet[Ether].dst
    return src_mac, dst_mac


def extract_ip_addresses(packet):
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    return src_ip, dst_ip
