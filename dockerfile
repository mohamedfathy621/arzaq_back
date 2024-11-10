# Use a Python 3.10 base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (including git)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port your Django app will run on
EXPOSE 8000

# Command to run Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
