
# Akvelon REST API

A REST API for storing user and transactions information. It is built using the flask framework, swagger module, sqlalchemy (for database managemnet with sqlite) and flask_restx (previously flask_restful)

## Testing
The REST API is tested using pytest with a coverage of 94%
![Pytest coverage](https://ibb.co/PF9nRTC)

To run the tests: Open terminal in project root folder and run
```bash
  pytest --cov
```
## Visit the deployed REST API at Heroku
https://akvelon-rest-api.herokuapp.com/

## Deployment with docker

Clone the GitHub repository:

```bash
  git clone git@github.com:dany-falta/akvelon_python_internship_3_Dani_Abulaila.git
```
Run in project directory:
```bash
docker-compose up --build
```

Visit the server at http://127.0.0.1:5000/ and interact with the swagger UI

## Run Locally

Clone the project

```bash
  git clone git@github.com:dany-falta/akvelon_python_internship_3_Dani_Abulaila.git
```

Go to the project directory

```bash
  cd akvelon_python_internship_3_Dani_Abulaila.git
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python wsgi.py
```
Visit the server at 
http://127.0.0.1:5000/
