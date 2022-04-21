import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('bot_token')
admin_id = os.getenv('admin_id')
apple_url = os.getenv('apple')
peach_url = os.getenv('peach')
db_address = os.getenv('DB_ADDRESS')
pg_user = os.getenv('PG_USER')
pg_pass = os.getenv('PG_PASS')
