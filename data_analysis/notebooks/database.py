# Création et manipulation de la base de données SQLite
import sqlite3
from sqlite3 import Error
import os


def create_database(db_name):
    """ Création de la base de données SQLite db_name
    """

    conn = None
    try:
        conn = sqlite3.connect(db_name)
        # Autorisation des clefs externes sur la base
        conn.execute("PRAGMA foreign_keys = 1")
        return conn
    except Error as e:
        print(e)

    return conn


def drop_table(db_name,table_name):
    
    conn = sqlite3.connect(db_name)
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Doppring table if already exists
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    print(f"Table dropped: {table_name}")

    #Commit your changes in the database
    conn.commit()

    return True
    
    
def create_table(db_name):
    """ Création des tables 
    """
    conn = sqlite3.connect(db_name)
    
    try:
        c = conn.cursor()
    
        # Création de la table `direction`
        c.execute('''CREATE TABLE IF NOT EXISTS direction 
                (id_direction INTEGER PRIMARY KEY,
                name_direction CHAR(30) NOT NULL)
                ''')
    
        # Création de la table `angle`
        c.execute('''CREATE TABLE IF NOT EXISTS angle 
                (id_angle INTEGER PRIMARY KEY, 
                values_angle REAL, 
                ND_direction INTEGER, 
                FOREIGN KEY (ND_direction) REFERENCES direction (id_direction))
                ''')
    
        # Création de la table `puissance`
        c.execute('''CREATE TABLE IF NOT EXISTS puissance 
                (id_puissance INTEGER PRIMARY KEY, 
                name_puissance CHAR(30) NOT NULL)
                ''')
    
        # Création de la table `throttle`
        c.execute('''CREATE TABLE IF NOT EXISTS throttle 
                (id_throttle INTEGER PRIMARY KEY, 
                values_throttle REAL, 
                NP_puissance INTEGER, 
                FOREIGN KEY (NP_puissance) REFERENCES puissance (id_puissance))
                ''')
    
        # Création de la table `circuit`
        c.execute('''CREATE TABLE IF NOT EXISTS circuit 
                (id_circuit INTEGER PRIMARY KEY, 
                name_circuit CHAR(50) NOT NULL) 
                ''')
    
        # Création de la table `path_image`
        c.execute('''CREATE TABLE IF NOT EXISTS path_images
                (id_path INTEGER PRIMARY KEY, 
                 path_image VARCHAR(200) NOT NULL)
                ''')
    
        # Création de la table `images`
        c.execute('''CREATE TABLE IF NOT EXISTS images 
                (id_image INTEGER PRIMARY KEY, 
                timestamp_ms INTEGER, 
                name_image CHAR(150) NOT NULL, 
                mode_pilot CHAR(50) NOT NULL, 
                date_ DATETIME, 
                NA_angle INTEGER, 
                NC_circuit INTEGER, 
                NT_throttle INTEGER, 
                FOREIGN KEY (NA_angle) REFERENCES angle (id_angle), 
                FOREIGN KEY (NC_circuit) REFERENCES circuit (id_circuit), 
                FOREIGN KEY (NT_throttle) REFERENCES throttle (id_throttle), 
                FOREIGN KEY (id_image) REFERENCES path_images (id_path))
                ''')
    
        # commit changes to db
        conn.commit()
        # close connection
        conn.close()
        
    except Error as e:
        print(e)
        c.close()


def check_table(db_name, table):
    
    # Connecion à la database
    conn = sqlite3.connect(db_name)
    
    cursor = conn.cursor()
    
    cursor_test = cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table}'")
    
        #if the count is 1, then table exists
    if cursor_test.fetchone()[0]==1 : 
        print(f"Table exists: {table}")
    else :
        print('Table {table} does not exist.')

    cursor_test.close()
    conn.close()
    
    
def insert(db_name, table, keys, values):
    
    connect = sqlite3.connect(db_name)
    curs = connect.cursor()

    
    vals = [f"'{str(v)}'" for v in values]
    #print("vals", vals)
    syntax = f"INSERT INTO {table} ({', '.join(keys)}) VALUES ({', '.join(vals)})" 
    #print(syntax)
    curs.execute(syntax)
    
    connect.commit()
    curs.close()
    connect.close()
    

