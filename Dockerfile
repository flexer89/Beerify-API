#official Python image as the base

FROM python:3.8-slim

# the workingSet directory inside

WORKDIR /app

#Copy the requirements.txt file to the working directory

COPY requirements.txt .

#Install dependencies

RUN apt-get update && apt-get install -y gcc && pip install --no-cache-dir -r requirements.txt

#Copy the rest of the files to the working directory

COPY . .

#Expose port 8000 for the FastAPI application

EXPOSE 8000

#Run the FastAPI application

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]