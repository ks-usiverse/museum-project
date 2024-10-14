FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install necessary dependencies for SQLite and clean up unnecessary files
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-dev \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the initial data file into the container
COPY ./initial_data.json /app/initial_data.json

# Expose the FastAPI port
EXPOSE 8000

# Set environment variables
ENV INITIAL_DATA_PATH=/app/initial_data.json

# Run database initialization and launch FastAPI using Uvicorn
CMD ["bash", "-c", "python init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
