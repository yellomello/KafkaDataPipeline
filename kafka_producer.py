import time
import json
from confluent_kafka import Producer
from data_source_movie_by_day import dataSourceMovieByDay
from data_source_movie_by_list import dataSourceMovieByList
from fetch_all_articles_for_movie import fetchAllArticlesForMovie

# Replace with your Kafka bootstrap server
bootstrap_servers = "localhost:9092"

# Create a Kafka producer
kafka_producer = Producer({'bootstrap.servers': bootstrap_servers})

# Function to handle producing messages
def produce_message(topic, message):
    kafka_producer.produce(topic=topic, value=message.encode())

def fetchMovieByListNewsData():
    movieByListNewsData = dataSourceMovieByList()
    print(movieByListNewsData)
    produce_message("movieByListNews", movieByListNewsData)

def fetchMovieByDayNewsData():
    movieByDayNewsData = dataSourceMovieByDay()
    print(movieByDayNewsData)
    produce_message("movieByDayNews", movieByDayNewsData)

def fetchNewsDataForAMovie(topic, movie):
    allArticlesForMovie = fetchAllArticlesForMovie(movie)
    produce_message(topic, allArticlesForMovie)

# Function to handle producing messages
def produce_message(topic, message):
    # Serialize the list of objects into a JSON string
    json_message = json.dumps(message)

    # Produce the message to the topic
    kafka_producer.produce(topic=topic, value=json_message.encode())

# Call the functions to fetch and produce data
# while True:
#     fetchMovieByDayNewsData()
#     fetchMovieByListNewsData()
#     kafka_producer.flush()
#     time.sleep(2)

#Call the functions to fetch and produce data
dictMovies = {'deadpoolAndWolverine': 'Deadpool & Wolverine', 'dunePartTwo': 'Dune: Part Two', 'kungFuPanda4': 'Kung Fu Panda 4', 'oppenheimer': 'Oppenheimer'}

for topic, movie in dictMovies.items():
    fetchNewsDataForAMovie(topic, movie)
    kafka_producer.flush()
    time.sleep(2)
