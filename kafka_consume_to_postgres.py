import psycopg2
from confluent_kafka import Consumer

# Replace with your Kafka bootstrap server and topic names
bootstrap_servers = "localhost:9092"
topic_names = ["sportsNews", "canadaNews", "movieByListNews", "movieByDayNews", "allArticlesForMovie"]

# Create a Kafka consumer
kafka_consumer = Consumer({'bootstrap.servers': bootstrap_servers, 'group.id': "my_group"})

# Subscribe to the topics
kafka_consumer.subscribe(topic_names)

# Connect to the PostgreSQL database
conn = psycopg2.connect(database="kafkaDatabase", user="postgres", password="VibekDutta@8890720", host="localhost", port="5432")
cur = conn.cursor()

# Function to insert data into the "customers" table
def insert_data(name, value, coin):
    print(name, value, coin)
    
    try:
        # Check if the table exists
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'customers')")
        table_exists = cur.fetchone()[0]

        if not table_exists:
            # If the table doesn't exist, create it
            cur.execute("""
                CREATE TABLE customers (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    value VARCHAR(255),
                    coin VARCHAR(50)
                )
            """)
            print("Table 'customers' created.")

        # Insert data into the customers table
        cur.execute("INSERT INTO customers (name, value, coin) VALUES (%s, %s, %s)", (name, float(value) if value else None, coin if coin else None))
        conn.commit()
        print("Data inserted successfully.")

    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()


# Poll for messages and insert data
arr=[0,0,0]
while True:
    msg = kafka_consumer.poll(timeout=1000)  # Adjust the timeout as needed

    if msg is None:
        continue
    if msg.error():
        print(f"Error: {msg.error()}")
        continue

    topic = msg.topic()
    value = msg.value().decode('utf-8')  # Decode the message

    
    if topic == "names":
        arr[0]=value
        # insert_data(value, None, None)  # Adjust parameters as needed
    elif topic == "coins":
        # insert_data(None, None, value)  # Adjust parameters as needed
        arr[2]=value
    elif topic == "values":
        # insert_data(None, value, None)  # Adjust parameters as needed
        arr[1]=value
    # Insert all three values at once when they are available (i.e., names's value, coins', and 'values' are not None)
        
        if all(i!=0 for i in arr):   # Check if all elements of array are nonzero
            insert_data(*arr)       # If yes, then insert them into the DB
            
    else:
        print(f"Unexpected Kafka message on topic '{topic}'")