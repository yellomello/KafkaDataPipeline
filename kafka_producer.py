import time
import requests
from confluent_kafka import Producer

# Replace with your Kafka bootstrap server
bootstrap_servers = "localhost:9092"

names_url = 'http://localhost:8100/api/names'
coins_url = 'http://localhost:8100/api/beta/whole/50/50'
values_url = 'http://localhost:8100/api/gaussian/whole/10/5'

# Create a Kafka producer
kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})

# Function to handle producing messages
def produce_message(topic, message):
    kafka_producer.produce(topic=topic, value=message.encode())

# Fetch data from the API and produce to the 'names' topic
def fetch_names():
    response = requests.get(names_url)
    name = response.json()['names']
    print(name)
    produce_message("names", name)

# Fetch data from the API and produce to the 'values' topic
def fetch_values():
    response = requests.get(values_url)
    value =  response.json()['values'][0]
    print(value)
    produce_message("values", value)

# Fetch data from the API and produce to the 'coins' topic
def fetch_coins():
    response = requests.get(coins_url)
    coin = response.json()["values"][0]
    print(coin)
    if coin == 0:
        produce_message(f"coins", "heads")
    else:
        produce_message(f"coins", "tails")

# Function to handle producing messages
def produce_message(topic, message):
    if not isinstance(message, str):
        message = str(message)
    kafka_producer.produce(topic=topic, value=message.encode())

# Call the functions to fetch and produce data
while True:
    fetch_names()
    fetch_coins()
    fetch_values()
    # Wait for all messages to be sent
    kafka_producer.flush()
    time.sleep(2)
