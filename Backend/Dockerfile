# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

EXPOSE 8080

# Run the application
CMD ["python", "server_rest.py"]
