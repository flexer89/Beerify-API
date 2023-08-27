# Beerify API

Beerify API is a FastAPI-based web application for collecting and managing beer reviews.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Usage](#usage)
- [Documentation](#endpoints)
- [License](#license)

## Introduction

Beerify API is designed to provide a platform for to manage beer reviews. It utilizes the FastAPI framework and SQLAlchemy for the database.

## Features

- Add, edit, and delete beer reviews
- Get beer reviews by ID, name, or other criteria
- Count and analyze beer reviews
- ...

## Usage

### Traditional way
1. Clone the repository:
```
git clone https://github.com/yourusername/beerify-api.git
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. run the API server:
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Using Docker
To start the container
```
start.sh
```

If you want to stop the container:
```
stop.sh
```

If you want to delete Docker container and image:
```
clear.sh
```

## Documentation
Access the API documentation at `http://localhost:8000/docs`

## License
This project is licensed under the MIT License.