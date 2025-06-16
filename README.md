# Network_Traffic_Storage

We save some meta-information fields (MAC addresses, IP addresses etc.) in ClickHouse, and archive the raw part of the packet using zstd.
Then you can assemble the packets into .pcap by the fields you need.

1. Cloning a repository

```git clone https://github.com/dmitryboris/Network_Traffic_Storage```

2. Creating a virtual environment

```python3 -m venv venv```

3. Activating the virtual environment

Windows:  
```venv\Scripts\activate```  
macOS / Linux:  
```source venv/bin/activate```

5. Install requirements

```pip3 install -r requirements.txt```

6. Run ClickHouse in Docker
   ```docker run -d --name clickhouse-server -p 9000:9000 -p 8123:8123 -p 9009:9009 -e CLICKHOUSE_DEFAULT_ACCESS_MANAGEMENT=1 -e CLICKHOUSE_USER=default -e CLICKHOUSE_PASSWORD= clickhouse/clickhouse-server```

8. Archive using archive.py
9. Compile using compile.py

