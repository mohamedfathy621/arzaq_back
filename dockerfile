# Step 1: Use the official Python image as a base image
FROM python:3.9-slim

# Step 2: Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Step 5: Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Step 6: Copy the entire project to the container (including frontend/dist for static files)
COPY . /app/

# Step 7: Expose port 8000 for the Django app
EXPOSE 8000

# Step 8: Collect static files (this includes your React `frontend/dist`)
RUN python manage.py collectstatic --noinput

# Step 9: Run the Django app (in development mode for local usage)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
