# Docker Image built using ChatGPT
# Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN python3 -m pip install --no-cache-dir .

# Expose the port that the FastAPI application will run on
EXPOSE 8005

# Define the command to run the FastAPI application
CMD ["uvicorn", "my_api.main:app", "--host", "0.0.0.0", "--port", "8005"]
