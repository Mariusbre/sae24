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

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion établie avec succès")
        client.subscribe("IUT/Colmar2023/SAE2.04/Maison1")
    else:
        print(f"Échec de la connexion. Code de retour : {rc}")


def check_id_exists(id):
    cursor.execute("SELECT IDs FROM capteurs WHERE IDs = %s", (id,))
    result = cursor.fetchone()
    return result is not None


def remove_duplicates():
    cursor.execute(
        """
        CREATE TEMPORARY TABLE temp_duplicates
        SELECT capteur_id, timestamp, degre
        FROM donnees
        GROUP BY capteur_id, timestamp, degre
        HAVING COUNT(*) > 1
        """
    )
    cursor.execute(
        """
        DELETE FROM donnees
        WHERE (capteur_id, timestamp, degre) IN (
            SELECT capteur_id, timestamp, degre
            FROM temp_duplicates
        )
        """
    )
    cursor.execute("DROP TABLE IF EXISTS temp_duplicates")

    db.commit()


def on_message(client, userdata, message):
    print(f"Message reçu : {message.payload}")

    a.add(message.payload.decode())
    for value in a:
        values = value.split(',')
        x = random.randint(0, 30)
        id = values[0]
        id = id.replace("Id=", "")
        capteur_id = values[0]
        capteur_id = capteur_id.replace("Id=", "")
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
            cursor.execute("INSERT INTO capteurs (IDs, nom_capteur, piece) VALUES (%s, %s, %s)",
                           (id, nom_capteur, piece))

        cursor.execute(
            "INSERT INTO donnees (capteur_id, timestamp, degre) VALUES (%s, %s, %s)", (capteur_id, timestamp, degre)
        )

        db.commit()
        z.append(id)
        remove_duplicates()


broker_address = "test.mosquitto.org"
client_id = str(uuid.uuid4())

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=1883, keepalive=60)
client.loop_forever()
