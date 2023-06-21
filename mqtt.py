from paho.mqtt import client as mqtt
import uuid
import csv
csv_file = "messages.csv"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connexion établie avec succès")
        client.subscribe("IUT/Colmar2023/SAE2.04/Maison1")
    else:
        print(f"Échec de la connexion. Code de retour : {rc}")


def on_message(client, userdata, message):
    print(f"Message reçu : {message.payload}")

    with open(csv_file, "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([message.payload.decode()])


broker_address = "test.mosquitto.org"
client_id = str(uuid.uuid4())

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, port=1883, keepalive=60)

client.loop_forever()