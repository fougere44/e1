# Course de voiture autonome IA-Racing !!! 
Ce répertoire vise rendre autonome un véhicule au format 1/16ème sur une vrai cricuit. Il a été mis en place dans le cadre de mon alternance chez le groupe SIGMA.


## Manipuler les *notebook* localement (sur votre machine)

1. Installez Anaconda sur votre machine (https://www.anaconda.com/products/individual)

2. Clonez le dépôt :
    ```
    git clone https://github.com/fougere44/e1.git
    ```

3. Déplacez-vous dans le répertoire du dépôt :
    ```
    cd e1/project
    ```

4. Créez l'environnement virtuel python :
    ```
    python -m venv env
    ```

5. Activez l'environnement virtuel "env" :
    ```
    cd env/Scripts
    activate
    ```
    
6. Installer les librairies :
    ```
    pip install -r requirements.txt
    ```

7. Chargez les extensions Jupyter Lab :

    - pour les utilisateurs de Linux, WSL, Mac :
    ```
    bash binder/postBuild
    ```
    
    - pour les utilisateurs de PowerShell :
    ```
    jupyter labextension install @jupyter-widgets/jupyterlab-manager
    jupyter labextension install @jupyterlab/toc
    ```

8. Lancez Jupyter Lab :
    ```
    jupyter lab
    ```


## Lancer l'application web Flask sur le port http://127.0.0.1:5000/ avec Visual Studio Code

1. Installez l'environnement de développement Visual Studio Code sur votre machine (https://code.visualstudio.com/)

2. Clonez le dépôt :
    ```
    git clone https://github.com/fougere44/e1.git
    ```

3. Déplacez-vous dans le répertoire du dépôt :
    ```
    cd e1/project
    ```

4. Lancer le projet sous Visual Studio Code avec le raccourci "code ."
   ```
    C:\Users\...\project\code .
    ```

5. Activez l'environnement virtuel "bank_env" :
    ```
    cd env/Scripts
    activate
    ```
    
6. Retourner dans le dossier "projet" :
    ```
    cd /
    cd C:\...\project
    ```

7. Définir les variables de l'application Flask :
    ```
    set FLASK_APP=run
    set FLASK_ENV=development
    flask run
    ```

8. Faire un ctrl + click à cette adresse : 
    ```
    http://127.0.0.1:5000/
    ```

9. Amusez-vous !


![alt text](https://i.ibb.co/9tBfs2f/Capture.png)


## Langages 

Jupyter notebooks / Python / HTML5 / CSS3


"# e1" 
