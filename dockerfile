# Use the official Python image from Docker Hub
FROM python:3.13-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY *py .

# Expose the port the app runs on
EXPOSE 5000

# Default command
CMD ["python", "main.py"]
