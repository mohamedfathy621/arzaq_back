FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies if necessary (e.g., for psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app files
COPY . .

# Expose the port your Django app will run on
EXPOSE 8000

# Command to run Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
