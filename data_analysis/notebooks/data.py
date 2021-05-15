import pandas as pd

df_direction = pd.read_csv('../data/dataframe_data/tables/table_direction.csv')
df_valeurs_angle = pd.read_csv('../data/dataframe_data/tables/table_valeurs_angle.csv')
df_puissance = pd.read_csv('../data/dataframe_data/tables/table_puissance.csv')
df_valeurs_throttle = pd.read_csv('../data/dataframe_data/tables/table_valeurs_throttle.csv')
df_circuit = pd.read_csv('../data/dataframe_data/tables/table_circuit.csv')
df_path = pd.read_csv('../data/dataframe_data/tables/table_path.csv')
df = pd.read_csv('../data/dataframe_data/tables/table_principale.csv')


df['date'] = pd.to_datetime(df['date'])
##
liste_ND_direction = []
    
for i in df_valeurs_angle["angle"]:
    if i < 0:
        liste_ND_direction.append(1)
    elif i == 0:
        liste_ND_direction.append(2)
    elif i > 0:
        liste_ND_direction.append(3)
            
df_valeurs_angle['ND_direction'] = liste_ND_direction
##

##
liste_NP_puissance = []

for i in df_valeurs_throttle["throttle"]:
    if i < 0:
        liste_NP_puissance.append(3)
    elif i == 0:
        liste_NP_puissance.append(2)
    elif i > 0:
        liste_NP_puissance.append(1)
    
df_valeurs_throttle['NP_puissance'] = liste_NP_puissance
##

##
liste_angle = []
liste_NA_angle = []

for i in df["user/angle"]:
    for j in df_valeurs_angle['angle']:
        if i == j:
            liste_angle.append(df_valeurs_angle.loc[df_valeurs_angle['angle'] == j].index.item())
            
    
for i in liste_angle:
    liste_NA_angle.append(i+1)
    
    
df['NA_angle'] = liste_NA_angle
del df['user/angle']
##

##
liste_throttle = []
liste_NT_throttle = []


for i in df["user/throttle"]:
    for j in df_valeurs_throttle['throttle']:
        if i == j:
            liste_throttle.append(df_valeurs_throttle.loc[df_valeurs_throttle['throttle'] == j].index.item())
            
for i in liste_throttle:
    liste_NT_throttle.append(i+1)
            
df['NT_throttle'] = liste_NT_throttle
del df['user/throttle']
##
    
##
liste_NC_circuit = []

for i in df["circuit"]:
    if i == "waveshare":
        liste_NC_circuit.append(1)
    
    elif i == "warehouse":
        liste_NC_circuit.append(2)

    elif i == "generated":
        liste_NC_circuit.append(3)
        
    else:
        liste_NC_circuit.append(4)
            
df['NC_circuit'] =  liste_NC_circuit
del df['circuit']
##
    

def get_data():
    # Données de la table direction
    direction = df_direction
    
    # Données de la table angle
    angle = df_valeurs_angle
    
    # Données de la table puissance
    puissance = df_puissance
     
    # Données de la table throttle
    throttle = df_valeurs_throttle
    
    # Données de la table circuit
    circuit = df_circuit
    
    # Données de la table path
    path = df_path
    
    # Données de la table images
    images = df
    
    return direction, angle, puissance, throttle, circuit, path, images
 
# Lorsque le fichier est appelé directement on exécute la fonction get_data
#if __name__ == "__main__":
#   get_data()