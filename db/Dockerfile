# Use the official Ubuntu 22.04 image as the base image
FROM ubuntu:latest

# Install MySQL server
RUN apt-get update && \
    apt-get install -y mysql-server && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the current directory to the working directory in the container
COPY . ./app

# Expose the default MySQL port
EXPOSE 3306

# Run the command to start the MySQL service
 CMD ["mysqld"]
