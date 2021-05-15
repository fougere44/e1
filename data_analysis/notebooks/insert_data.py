from database import *
from data import *
import sqlite3

#path_env = "C:\Users\afougere\Anaconda3\envs\IA-Racing"

# nom de la base de données : iaracing.db
#path_db = "C:/Users/afougere/Git/racing_project/data_mysim/stockage_bdd/"
db_name = '../stockage_bdd/iaracing.db'

# Création de la base de données et des sept tables
create_database(db_name)

# Suprresion des tables si elles existent déjà dans la base de données iaracing.db
liste_tables = ['direction', 'angle', 'puissance', 'throttle', 'circuit', 'path_images', 'images']

for i in liste_tables:
    drop_table(db_name, i)


# Création des sept tables dans ma base de données iaracing.db
create_table(db_name)

# Vérification de l'existence de chaque table en base de données iaracing.db
for i in liste_tables:  
    check_table(db_name, i)

# Insertion des données

for direction in range(len(df_direction)):
    insert(db_name, 'direction', ["name_direction"], [df_direction['direction'][direction]])
    
for i in range(len(df_puissance)): 
    insert(db_name, 'puissance', ["name_puissance"], [df_puissance['puissance'][i]])
    
for circuit in range(len(df_circuit)):
    insert(db_name, 'circuit', ["name_circuit"], [df_circuit['circuit'][circuit]])

for value in range(len(df_valeurs_angle)):
    insert(db_name, 'angle', ["values_angle", "ND_direction"], [df_valeurs_angle['angle'][value], df_valeurs_angle['ND_direction'][value]])
    
for value in range(len(df_valeurs_throttle)):
    insert(db_name, 'throttle', ["values_throttle", "NP_puissance"], [df_valeurs_throttle['throttle'][value], df_valeurs_throttle['NP_puissance'][value]])
    
for path in range(len(df_path)):
    insert(db_name, 'path_images', ["path_image"], [df_path['path'][path]])
    
for value in range(len(df)):
    insert(db_name, 'images', ["timestamp_ms", "name_image", "mode_pilot", "date_", "NA_angle", "NC_circuit", "NT_throttle"], [df["timestamp_ms"][value], df["cam/image_array"][value], df["user/mode"][value], df["date"][value], df["NA_angle"][value], df["NC_circuit"][value], df["NT_throttle"][value]]) 


