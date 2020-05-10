# Full Stack Capstone Final Project

## Innovate App

This simple app creates projects, allows people to check in, and add and edit projects. It's a good example of a Single Page Application which includes connection to a database using SQLAlchemy, RESTful API development, Role Based Authentication and roles and deployment using Heroku. It's a practical way to learn everything covered in this Full Stack Nanodegree course. This app is capable of performing the tasks below:

1. Display a list of projects for a team in a company organization.
2. Display project details.
3. Display a list of all team members with their corresponding projects.
4. Add new projects.
5. Edit details of an existing project.
6. Delete an existing project.

This project will give the ability to structure plan, implement, and test an API - skills essential for enabling future applications to communicate with others.

## Getting Started

### Pre-requisite and Local Development

The development code can be found on the Github [project repository](https://github.com/opcreek/Innovate).

To run locally, import the psql dump file `inno.psql` locally and install the dependencies using the `requirments.txt` file.

### Backend

The `./backend` directory contains the Flask and SQLAlchemy server. To run the api, run the following commands from the backend directory:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### Tests

To run the tests, navigate to the backend folder and run the following commands:

```
createdb inno_test
psql: inno_test < inno.psql
python test_app.py
```

## API Referrence

### Getting Started

- Base URL: The backend app is hosted at [Heroku](https://innorey.herokuapp.com/).
- Authentication: This app uses third-party authentication. The third party service used is **Autho**.

### Error Handling

The api will return the following errors when request fails:

- 404: Resource Not Found

```
    {
          "success": False,
          "error": 404,
          "message": "resource not found"
    }
```

- 422: Unprocessable

```
    {
          "success": False,
          "error": 422,
          "message": "unprocessable"
    }
```

- 400: Bad Request

```
    {
          "success": False,
          "error": 400,
          "message": "bad request"
    }
```

- 400: Bad Request

```
    {
          "success": False,
          "error": 400,
          "message": "bad request"
    }
```

- 403: Permission not found

```
    {
          "success": False,
          "error": 403,
          "message": "Permission not found"
    }
```

- 401: Unauthorized

```
    {
          "success": False,
          "error": 401,
          "message": "Unauthorized"
    }
```

## Endpoints

### GET /project

- This endpoint handles GET requests for all current projects. This endpoint will return a list of all project title.

### GET /questions

- This endpoint handles GET requests for questions, including pagination per 10 questions. This endpoint will return a list of questions, number of total questions and list of categories.

### DELETE /questions/\<int:id>

- This endpoint will delete a question using the question ID. This will return a boolean result whether successful deletion: True or failed deletion: False. This endpoint will also return the question id that was deleted.

### POST /questions

- This endpoint will allow for posting a new question including the requirements for the answer text, category and difficulty score. This endpoint will return the following: a boolean result whether successful submission: True or failed submission: False, the new question id, the new quesstion, a paginated list of the current questions and the total number of questions.

### POST /questions/search

- This endpoint will search for all questions based on a search term. This endpoint will return any questions which contain the string specified in the search term paginated if needed. It will also return a boolean result whether successful search: True or failed search: False and the total number of questions. It is also case-insensitive.

### GET /categories/\<int:id>/questions

- This endpoint will get all questions based on a category. This endpoint will return a boolean result whether successful retrieval: True or fail: False, a paginated result with 10 questions per page and the current category.

### POST /quizzes

- This endpoint will get questions to play the trivia. This endpoint will return a random question within the given category if provided or for all categories. This endpoint also has the capability to make sure that the current selection is not the previous questions used.

## Deployment: N/A

## Author

Renante Ramas
