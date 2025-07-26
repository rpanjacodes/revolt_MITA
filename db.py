import asyncpg

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user="your_pg_user",          # 🔁 Replace this
            password="your_pg_password",  # 🔁 Replace this
            database="your_pg_db",        # 🔁 Replace this
            host="localhost",             # Or your DB host/IP
            port=5432
        )

    async def setup_tables(self):
        await self.pool.execute("""
            CREATE TABLE IF NOT EXISTS chatbot_channels (
                server_id TEXT PRIMARY KEY,
                channel_id TEXT NOT NULL
            );
        """)

    async def set_chatbot_channel(self, server_id: str, channel_id: str):
        await self.pool.execute("""
            INSERT INTO chatbot_channels (server_id, channel_id)
            VALUES ($1, $2)
            ON CONFLICT (server_id)
            DO UPDATE SET channel_id = EXCLUDED.channel_id;
        """, server_id, channel_id)

    async def get_chatbot_channel(self, server_id: str):
        row = await self.pool.fetchrow("""
            SELECT channel_id FROM chatbot_channels
            WHERE server_id = $1
        """, server_id)
        return row["channel_id"] if row else None

    async def remove_chatbot_channel(self, server_id: str):
        await self.pool.execute("""
            DELETE FROM chatbot_channels
            WHERE server_id = $1
        """, server_id)
