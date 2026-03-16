import mysql.connector


def make_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='actowiz',
        database='wendy'
    )
    return conn

def create_table(table_name: str):

    create_query = f'''
    CREATE TABLE IF NOT EXISTS {table_name}(
        id INT AUTO_INCREMENT PRIMARY KEY,

        brand_name VARCHAR(100),
        branch_name VARCHAR(255),
        store_id VARCHAR(50),

        cuisine VARCHAR(100),
        price VARCHAR(10),

        street_address VARCHAR(255),
        city VARCHAR(100),
        state VARCHAR(50),
        postalcode VARCHAR(20),
        country VARCHAR(50),

        latitude DECIMAL(10,7),
        longitude DECIMAL(10,7),

        phone_number VARCHAR(50),

        restaurant_hours JSON,
        amenities JSON,
        delivery_partners JSON,

        meta_description TEXT,
        source_url TEXT

    )
    '''

    conn = make_connection()
    cursor = conn.cursor()

    cursor.execute(create_query)

    conn.commit()
    conn.close()

def insert_into_db(table_name: str, data: dict):
    cols = ",".join(list(data.keys()))
    vals = "".join([len(data.keys()) * '%s,']).strip(',')
    q = f"""INSERT INTO {table_name} ({cols}) VALUES ({vals})"""
    conn = make_connection()
    cursor = conn.cursor()
    cursor.execute(q, tuple(data.values()))
    conn.commit()
