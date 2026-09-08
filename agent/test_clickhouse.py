import os
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()

client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST"),
    user=os.getenv("CLICKHOUSE_USER"),
    password=os.getenv("CLICKHOUSE_PASSWORD"),
    secure=os.getenv("CLICKHOUSE_SECURE", "true").lower() == "true"
)

result = client.query("SELECT 1").result_set[0][0]

print("ClickHouse connection successful!")
print("Result:", result)