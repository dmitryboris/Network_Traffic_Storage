import tarfile
import io
import zstandard as zstd
from scapy.layers.l2 import Ether
from scapy.utils import RawPcapReader, PcapWriter
from config import PCAP_PATH, ARCHIVE_PATH, BATCH_SIZE, RESTORED_PCAP_PATH
from utils import get_timestamp
from db import insert_batch, load_next_batch


def process_pcap():
    batch = []
    with open(ARCHIVE_PATH, 'wb') as f_out:
        cctx = zstd.ZstdCompressor(level=10)
        with cctx.stream_writer(f_out) as zstd_stream:
            with tarfile.open(mode='w|', fileobj=zstd_stream) as tar:
                for i, (pkt, pkt_metadata) in enumerate(RawPcapReader(PCAP_PATH)):

                    packet_data = (i, get_timestamp(pkt_metadata), pkt_metadata.wirelen)
                    batch.append(packet_data)

                    if len(batch) >= BATCH_SIZE:
                        insert_batch(batch)
                        batch = []

                    raw_buf = io.BytesIO(pkt)
                    raw_info = tarfile.TarInfo(name=f"{i}_packet.raw")
                    raw_info.size = len(pkt)
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
