import asyncio
import asyncpg
from config import settings


async def create_table():
    result = {}
    conn = await asyncpg.connect(user=settings.db.username, 
                                 password=settings.db.password, 
                                 host=settings.db.host,
                                 database=settings.db.database, 
                                 port=settings.db.port)
    
    table_servers = await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS servers (
        id SERIAL PRIMARY KEY,
        name TEXT,
        server_dc_id BIGINT,
        members INTEGER,
        is_gathering_stats BOOLEAN
        )
        """
    )
    
    table_users = await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        user_dc_id BIGINT,
        username TEXT,
        last_join_vc TIMESTAMP,
        join_server DATE,
        server_id INTEGER REFERENCES servers (id)
        )
    """)
    
    table_stats = await conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_stats (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users (id),
        day_stats DATE,
        voice_time INTERVAL,
        messages INTEGER
        )
        """
    )
    
    table_users_info = await conn.fetch("""
        SELECT * FROM information_schema.columns
        WHERE table_name = 'users'
    """)
    
    table_users_stats_info = await conn.fetch("""
        SELECT * FROM information_schema.columns
        WHERE table_name = 'user_stats'
    """)

    table_servers_info = await conn.fetch("""
        SELECT * FROM information_schema.columns
        WHERE table_name = 'servers'
    """)
    
    await conn.close()
    # CHECK IF TABLE CREATED AND PRINTS INFO ABOUT TABLES
    result = {'users': {}}
    for i in table_users_info:
        result['users'][i['column_name']] = i['data_type']
    print(f'{result}\n')
    
    result = {'users_stats': {}}  
    for i in table_users_stats_info:
        result['users_stats'][i['column_name']] = i['data_type']
    print(f'{result}\n')

    result = {'servers': {}}
    for i in table_servers_info:
        result['servers'][i['column_name']] = i['data_type']
    print(f'{result}\n')

    await conn.close()

    return table_users



async def start_gathering(name, server_dc_id, members, is_gathering_stats):
    conn = await asyncpg.connect(user=settings.db.username, 
                                 password=settings.db.password, 
                                 host=settings.db.host,
                                 database=settings.db.database, 
                                 port=settings.db.port)
    
    try:
        sql_str = f"""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM servers WHERE server_dc_id = {server_dc_id}) THEN
                INSERT INTO servers (name, server_dc_id, members, is_gathering_stats)
                VALUES ('{name}', {server_dc_id}, {members}, {is_gathering_stats});
            ELSE
                UPDATE servers
                SET is_gathering_stats = {is_gathering_stats};   
            END IF;
        END $$;
    """
        some_sql = await conn.execute(sql_str)
    except Exception as e:
        print(e)
    

    some_sql = await conn.fetch("""SELECT * FROM servers""")
    print(some_sql)

    await conn.close()


async def stop_gathering(server_dc_id):
    conn = await asyncpg.connect(user=settings.db.username, 
                                 password=settings.db.password, 
                                 host=settings.db.host,
                                 database=settings.db.database, 
                                 port=settings.db.port) 

    some_sql = await conn.execute(f"""
        UPDATE servers
        SET is_gathering_stats = False
        WHERE server_dc_id = {server_dc_id};
    """)   

    some_sql = await conn.fetch("""SELECT * FROM servers""")
    print(some_sql)

    await conn.close()


# ДЛЯ РАЗРАБОТЧИКА
async def admin_delete_table(table):
    conn = await asyncpg.connect(user=settings.db.username, 
                                 password=settings.db.password, 
                                 host=settings.db.host,
                                 database=settings.db.database, 
                                 port=settings.db.port)
    
    some_sql = await conn.execute(f"""
                                DROP TABLE {table} CASCADE
                            """)
    
    await conn.close()



async def admin_truncate_table(table):
    conn = await asyncpg.connect(user=settings.db.username, 
                                 password=settings.db.password, 
                                 host=settings.db.host,
                                 database=settings.db.database, 
                                 port=settings.db.port) 
    some_sql = await conn.execute(f"""TRUNCATE TABLE servers CASCADE""")

    some_sql = await conn.fetch(f"""SELECT * FROM servers""")

    print(some_sql)

# loop = asyncio.new_event_loop()
# loop.run_until_complete(admin_truncate_table('servers'))
# loop.run_until_complete(stop_gathering(1231231))

# loop.run_until_complete(admin_delete_table('user_stats'))
# loop.run_until_complete(admin_delete_table('users'))
# loop.run_until_complete(admin_delete_table('servers'))
# loop.run_until_complete(create_table())

