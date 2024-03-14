import csv
import nltk
import json
from nltk.data import find
from confluent_kafka import Consumer
from nltk.sentiment import SentimentIntensityAnalyzer

# Check if the VADER lexicon is already downloaded
if not find("sentiment/vader_lexicon.zip"):
    nltk.download('vader_lexicon')

# Replace with your Kafka bootstrap server and topic names
bootstrap_servers = "localhost:9092"
topic_names = ["deadpoolAndWolverine", "dunePartTwo", "kungFuPanda4", "oppenheimer"]

# Create a Kafka consumer
kafka_consumer = Consumer({'bootstrap.servers': bootstrap_servers, 'group.id': "my_group"})

# Subscribe to the topics
kafka_consumer.subscribe(topic_names)

sid = SentimentIntensityAnalyzer()  # Sentiment analyzer

# Define the CSV file path to write the incoming data
csv_file_path = "movie_news_sentiment.csv"

# Create a dictionary to store CSV writers for each topic
csv_writers = {}

# Open CSV file and create CSV writers for each topic
with open(csv_file_path, 'a+') as csv_file:
    for topic in topic_names:
        csv_writer = csv.DictWriter(csv_file, fieldnames=['source', 'author', 'title', 'url', 'publishedAt', 'content', 'sentiment', 'movie'], extrasaction='ignore')
        csv_writers[topic] = csv_writer

    # Check if the file is empty
    csv_file.seek(0)
    is_existing_file = csv_file.read(1) != ''

    # Write the headers if the file is empty
    if not is_existing_file:
        csv_writer.writeheader()

    # Poll for messages and process data
    while True:
        msg = kafka_consumer.poll(timeout=1000)

        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
            continue

        topic = msg.topic()

        # Decode the message value from bytes to string
        message_value = msg.value().decode()

        try:
            # Deserialize the JSON string into a list of objects
            decoded_message = json.loads(message_value)

            # Process the decoded message
            for obj in decoded_message:
                print(f"\n\n{topic}", obj['content'])
                sentiment_score = sid.polarity_scores(obj['content'])
                obj['sentiment'] = sentiment_score['compound']
                if topic == "deadpoolAndWolverine":
                    obj['movie'] = "Deadpool vs Wolverine"
                elif topic == "dunePartTwo":
                    obj['movie'] = "Dune: Part Two"
                elif topic == "kungFuPanda4":
                    obj['movie'] = "Kung Fu Panda 4"
                elif topic == "oppenheimer":
                    obj['movie'] = "Oppenheimer"

                # Write the object data to the corresponding CSV writer
                csv_writer = csv_writers.get(topic)
                if csv_writer is not None:
                    csv_writer.writerow(obj)

            # Flush the CSV writers to ensure data is written to the file
            csv_file.flush()

        except json.JSONDecodeError:
            print(f"Failed to decode message: {message_value}")

        # Check if all topics have been consumed
        if all((csv_writer is not None and csv_writer.line_num == kafka_consumer.committed(msg)) for csv_writer in csv_writers.values()):
            break

# Close the Kafka consumer session
kafka_consumer.close()
print("Done")