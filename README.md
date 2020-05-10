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

## API Referrence

### Getting Started

- Base URL: The backend app is hosted at [Heroku](https://innorey.herokuapp.com/) - `https://innorey.herokuapp.com/`
- Authentication: This app uses third-party authentication. The third party service used is **Autho**.

### Pre-requisite and Local Development

The development code can be found on the Github [project repository](https://github.com/opcreek/Innovate).

To run locally, import the psql dump file `inno.psql` locally and install the dependencies using the `requirements.txt` file.

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

Authentication is also utilized in the testing based on 3 primary roles. The token variables found in the `auth.py` file has been initially filled out and should be good for the next 24 hours. Please generate new tokens if the tokens has expired and replace the current values for the token variables listed below with the new tokens generated.

- `INT_token`
- `EMP_token`
- `SUP_token`

## Authentication

This app utilizes the third party authentication service **Auth0**. Three RBAC roles are enabled and setup as follows:

1.  Intern - general access/no permissions assigned

    - `email: test123@email.com`
    - `password: Password123!`

2.  Employee - limited access, end points allowed:

    ```
    get:project:detail
    patch:project
    post:project
    ```

    - `email: innovate_empl@me.com`
    - `password: Password456!`

3.  Supervisor - full access, end points allowed:

    ```
    get:project:detail
    get:team-members
    patch:project
    post:project
    delete:project
    ```

    - `email: innovate_sup@icloud.com`
    - `password: Password678!`

Note: The JWT token generated only has a maximum 24 hours lifetime. To generate a new token, open a new browser and enter the url:

```
https://dev-fsnd-15.auth0.com/authorize?audience=innovateProject&response_type=token&client_id=6VxACGsal1QLpAmhV6hwYFkjej81UQV0&redirect_uri=http://localhost:3000
```

Email and password are provided above for the role desired.

## Endpoints

### GET `/`

- This endpoint is the landing page and will just display the welcome string.

### GET `/project`

- This endpoint handles GET requests for all current projects. This endpoint will return a list of all project title.

### GET `/projects/<int:proj_id>/details`

- This endpoint handles GET requests for project details. This endpoint will return items of the projects such as project id, title, start date, end date, description and completed status.

### GET `/members`

- This endpoint handles GET requests for all current team members. This endpoint will return a list of members in the team assigned to projects. This endpoint will require authorization based on RBAC roles setup for this endpoint.

### DELETE `/projects/<int:id>`

- This endpoint will delete a project using the project ID. This will return a boolean result whether successful deletion: True or failed deletion: False. This endpoint will require authorization based on RBAC roles setup for this endpoint.

### POST `/projects`

- This endpoint will allow for posting of a new project including the requirements for the project title, start date, end date, description and completed status. This endpoint will return the following: a boolean result whether successful submission: True or failed submission: False, new project id, new project title, new start date, new description, new completed status and the new total number of projects. This endpoint will require authorization based on RBAC roles setup for this endpoint.

### PATCH `/projects/<int:proj_id>`

- This endpoint will allow for editing particular items in a project. The items that can be edited are the project end date, description and completed status. This endpoint will return the following: a boolean result whether successful edit: True or failed edit: False, the project id that was edited, the project title, the project start date, the new end date, the new description and the new completed status. This endpoint will require authorization based on RBAC roles setup for this endpoint.

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

## Deployment:

This API is hosted in Heroku. Base URL: [Heroku](https://innorey.herokuapp.com/) - `https://innorey.herokuapp.com/`

To test endpoints at live application endpoint, a postman collection json file - `Innovate Test.postman_collection.json` is provided in the backend directory that can be imported to postman if desired.

## Author

Renante Ramas
