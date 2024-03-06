# Use an official Node.js image as a parent image
FROM node:14

# Set the working directory to /app
WORKDIR /app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install app dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Build the TypeScript code
RUN npm run build

# Make port 8099 available to the world outside this container
EXPOSE 8099

# Run the server
CMD ["npm", "start"]
