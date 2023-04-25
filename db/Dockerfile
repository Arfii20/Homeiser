# Use the official Ubuntu 22.04 image as the base image
FROM ubuntu:latest

# Install MySQL server
RUN apt update && \
    apt install -y mysql-server && \
    apt clean

RUN apt install -y systemctl

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the current directory to the working directory in the container
COPY . .

# Expose the default MySQL port
EXPOSE 3306

CMD ["/bin/bash"]
CMD ["systemctl", "start", "mysql.service"]
