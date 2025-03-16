# Choose a base image with Python
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install Django dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV SECRET_KEY=${SECRET_KEY_DJANGO}

# Expose port 8000 for Django
EXPOSE 8000

# Run the Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
