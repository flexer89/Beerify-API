# Use the official Python image as the base
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files to the working directory
COPY . .

# Run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
