# Kafka to PostgreSQL Data Pipeline

This project demonstrates a simple data pipeline that consumes messages from Kafka topics and inserts the data into a PostgreSQL database. The Kafka topics used in this example are names, values, and coins.

- Run a Docker container with Apache Zookeeper and Apache Kafka Broker configured. Additionally, set up a PostgreSQL database within the container.
- Launch a NodeJS application server that provides custom API endpoints.
- The Kafka Producer retrieves data from these API endpoints and publishes messages to Kafka topics named "names," "values," and "coins."
- The Kafka Consumer subscribes to these topics, captures the data, and stores it in a PostgreSQL database in the “customers” table.

## Project Files

docker-compose.yml: This YAML file represents a Docker Compose configuration for orchestrating several services in a containerized environment. Here's a breakdown of the services defined:

### Kafka:

1. zookeeper: Utilizes the official Confluent Zookeeper image, configuring the client port and tick time.

2. broker: Utilizes the official Confluent Kafka image, setting up the broker with specific ports, dependencies on Zookeeper, and various Kafka environment variables for configuration.

### Database:

1. database: Uses the official PostgreSQL image with version 15.0-alpine3.16. Configures a PostgreSQL database with a specified password and database name, exposing the container's port 5432 for external access.

### Server:

1. server: Builds a Docker image from the ./app directory using the specified Dockerfile. This service represents a custom server, likely a Flask application, exposing port 8099. It depends on the database service.

This configuration essentially sets up a local development environment with Kafka, PostgreSQL, and a custom server that interacts with the Kafka topics and database. The docker-compose.yml file coordinates these services and their dependencies, allowing for easy deployment and management within Docker containers.
