import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ADMIN_ID')
apple_url = os.getenv('APPLE')
peach_url = os.getenv('PEACH')
db_address = os.getenv('DB_ADDRESS')
pg_user = os.getenv('PG_USER')
pg_pass = os.getenv('PG_PASS')

