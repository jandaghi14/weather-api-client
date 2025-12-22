import sqlite3
DB_Name = "cache.db"
def get_connection():
    conn= sqlite3.connect(DB_Name)
    return conn
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS weather_cache(
                       city TEXT PRIMARY KEY,
                       temperature REAL,
                       humidity INTEGER,
                       description TEXT,
                       cached_at TEXT
                   )
                   """)
    
    
    conn.commit()
    conn.close()

create_table()


def get_all_cache():
    conn = get_connection()
    cursor = conn.cursor()
    result = cursor.execute("""
                    SELECT * FROM weather_cache 
                    """).fetchone()
    conn.close()
    return result
def chech_cache(city):
    conn = get_connection()
    cursor = conn.cursor()
    result = cursor.execute("""
                    SELECT * FROM weather_cache WHERE city = ?
                    """,(city,)).fetchone()
    conn.close()
    return result
def add_weather(city , temperature, humidity, description, cached_at):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                            INSERT INTO weather_cache (city , temperature , humidity , description , cached_at)
                            VALUES (?,?,?,?,?)
                            """,(city, temperature , humidity , description , cached_at))
    conn.commit()
    conn.close() 
def update_cache_weather(city , temperature, humidity, description, cached_at):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                            UPDATE weather_cache  SET temperature=? , humidity=? , description=? , cached_at=?
                            WHERE city = ?
                            """,(temperature , humidity , description , cached_at, city))
    conn.commit()
    conn.close() 





