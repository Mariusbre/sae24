import random
import time
import uuid
import mysql.connector
import datetime
from paho.mqtt import client as mqtt

a = set()
z = []
connected = False

while not connected:
    try:
        db = mysql.connector.connect(
            host="10.252.17.139",
            user="toto",
            password="Toto1234@",
            database="grp17",
        )
        connected = True
    except mysql.connector.Error as erreur:
        print("Erreur de connexion:", erreur)
        time.sleep(2)

cursor = db.cursor()
cursor.execute("""
SELECT 1 FROM capteurs LIMIT 1
""")
existe_pas = cursor.fetchone() is None

if existe_pas:
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE grp17")
    cursor.execute("USE grp17")

    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS capteurs (
        ID VARCHAR(255) NOT NULL,
        nom_capteur VARCHAR(255),
        piece VARCHAR(50) NOT NULL,
        UNIQUE (nom_capteur),
        PRIMARY KEY (ID))
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donnees (
        id INT NOT NULL AUTO_INCREMENT,
        capteur_id VARCHAR(255) NOT NULL,
        CONSTRAINT capteursFK
            FOREIGN KEY (capteur_id)
            REFERENCES capteurs(ID),
        timestamp DATETIME NOT NULL,
        degre FLOAT NOT NULL,
        PRIMARY KEY (id))
    """)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion établie avec succès")
        client.subscribe("IUT/Colmar2023/SAE2.04/Maison1")
    else:
        print(f"Échec de la connexion. Code de retour : {rc}")


def check_id_exists(id):
    cursor.execute("SELECT ID FROM capteurs WHERE ID = %s", (id,))
    result = cursor.fetchone()
    return result is not None


def on_message(client, userdata, message):
    print(f"Message reçu : {message.payload}")

    a.add(message.payload.decode())
    for value in a:
        values = value.split(',')
        x = random.randint(0, 30)
        id = values[0]
        id = id.replace("ID=", "")
        capteur_id = values[0]
        capteur_id = capteur_id.replace("ID=", "")
        piece = values[1]
        piece = piece.replace("piece=", "")
        date = values[2]
        date = date.replace("date=", "")
        heure = values[3]
        heure = heure.replace("time=", "")
        degre = values[4]
        degre = degre.replace("temp=", "")
        nom_capteur = piece + str(x)
        timestamp = datetime.datetime.strptime(f"{date} {heure}", "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        if id in z or check_id_exists(id):
            c = 4
        else:
            cursor.execute("INSERT INTO capteurs (id, nom_capteur, piece) VALUES (%s, %s, %s)",
                           (id, nom_capteur, piece))

        cursor.execute(
            "INSERT INTO donnees (capteur_id, timestamp, degre) VALUES (%s, %s, %s)", (capteur_id, timestamp, degre)
        )

        db.commit()
        z.append(id)


broker_address = "test.mosquitto.org"
client_id = str(uuid.uuid4())

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=1883, keepalive=60)
client.loop_forever()
