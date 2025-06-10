import tarfile
import io
import zstandard as zstd
from scapy.layers.l2 import Ether
from scapy.utils import RawPcapReader, PcapWriter
from config import PCAP_PATH, ARCHIVE_PATH, BATCH_SIZE, RESTORED_PCAP_PATH
from utils import get_timestamp, extract_mac_addresses, extract_ip_addresses
from db import insert_batch, load_next_batch, get_archive_paths_by_dst_ip, get_packets_by_archive_path


def process_pcap():
    batch = []
    with open(ARCHIVE_PATH, 'wb') as f_out:
        cctx = zstd.ZstdCompressor(level=10)
        with cctx.stream_writer(f_out) as zstd_stream:
            with tarfile.open(mode='w|', fileobj=zstd_stream) as tar:
                for i, (pkt_bytes, pkt_metadata) in enumerate(RawPcapReader(PCAP_PATH)):
                    pkt = Ether(pkt_bytes)
                    src_mac, dst_mac = extract_mac_addresses(pkt)
                    src_ip, dst_ip = extract_ip_addresses(pkt)
                    packet_data = (
                        ARCHIVE_PATH, i, get_timestamp(pkt_metadata), pkt_metadata.wirelen, src_mac, dst_mac, src_ip,
                        dst_ip
                    )
                    batch.append(packet_data)

                    if len(batch) >= BATCH_SIZE:
                        insert_batch(batch)
                        batch = []

                    raw_buf = io.BytesIO(pkt_bytes)
                    raw_info = tarfile.TarInfo(name=f"{i}_packet.raw")
                    raw_info.size = len(pkt_bytes)
                    tar.addfile(raw_info, raw_buf)

                if batch:
                    insert_batch(batch)


def compile_pcap():
    batch_idx = 0
    offset = 0
    batch = load_next_batch(offset, BATCH_SIZE)

    with open(ARCHIVE_PATH, 'rb') as f_in, PcapWriter(RESTORED_PCAP_PATH, append=False, sync=True, linktype=1) as pcap:
        dctx = zstd.ZstdDecompressor()
        pcap.write_header(None)
        with dctx.stream_reader(f_in) as zstd_stream:
            with tarfile.open(mode='r|', fileobj=zstd_stream) as tar:
                for i, member in enumerate(tar):
                    if member.isfile():
                        # index = int(member.name.split("_")[0])
                        if i // BATCH_SIZE > batch_idx:
                            offset += BATCH_SIZE
                            batch = load_next_batch(offset, BATCH_SIZE)
                            batch_idx += 1

                        raw_packet = tar.extractfile(member).read()

                        _, timestamp, wirelen = batch[i % BATCH_SIZE]

                        if timestamp is None:
                            continue

                        pkt = Ether(raw_packet)
                        pkt.time = timestamp

                        pcap.write_packet(
                            pkt,
                            wirelen=wirelen  # без него пакеты битые
                        )


def compile_pcaps(dst_ip=None, src_ip=None, src_mac=None, dst_mac=None):
    archive_paths = get_archive_paths_by_dst_ip(dst_ip, src_ip, src_mac, dst_mac)
    print(archive_paths)
    with PcapWriter(RESTORED_PCAP_PATH, append=False, sync=True, linktype=1) as pcap:
        pcap.write_header(None)
        for archive_path in archive_paths:
            packets_data = get_packets_by_archive_path(archive_path, dst_ip, src_ip, src_mac, dst_mac)
            with open(archive_path, 'rb') as f_in:
                with zstd.ZstdDecompressor().stream_reader(f_in) as zstd_stream:
                    with tarfile.open(mode='r|', fileobj=zstd_stream) as tar:
                        for i, member in enumerate(tar):
                            data = packets_data.get(i, None)
                            if not data:
                                continue

                            raw_packet = tar.extractfile(member).read()
                            timestamp, wirelen = data

                            pkt = Ether(raw_packet)
                            pkt.time = timestamp

                            pcap.write_packet(
                                pkt,
                                wirelen=wirelen
                            )
