







## Motivation for project

The idea for this project is to do an app that will connect studio and gym owners with fitness instructors.  Since COVID19 started, most 
fitness companies have gone online.  They now can hire from all over the world to present classes.  This is the backend to that app. 

The app has three user types - a business owner, a manager, and an assistant.  The owner can do everything.  The manager can do most things except add studios. They can add and edit instructors.  Assistants can only get instructors and studios.  

## Project dependencies, local development and hosting instructions,

Clone this repo and create your local test and development databases with the following names.

    studios     
    studios_test

    Install project dependencies:- pip install -r requirements.txt

    Load environment variables:- source setup.sh

    Run the database migrations:- python3 manage.py db upgrade
    
    Seed tables with some initial data:- python3 manage.py seed

    Run the application:- flask run

    The app is served on port 5000


## Technologies

    - Python/Flask
    - Flask-Migrate
    - Flask-Cors
    - Flask-Script
    - Auth0
    - SQLAlchemy
  

## Detailed instructions for scripts to install any project dependencies, and to run the development server.
[Heroku Link](https://studioshub-api.herokuapp.com/)

[login](https://tomariken.auth0.com/authorize?audience=studios&response_type=token&client_id=4B2JZKN2Zsgmxx3a7A90RdsubfTfhVNC&redirect_uri=http://localhost:8080/login-results) |
[logout](https://tomariken.auth0.com/v2/logout)


    To access the endpoints in the next section, you'll need to be logged-in.
    The app uses a third-party service (Auth0) for authentication.
    Three roles (user-types) have been created on Auth0. To login as any of these, use the following login details

    Business Owner          maxamillion@gmail.com Password: fair123!
    Manager       l         loislane@gmail.com Password: fair123!
    Casting Assistant       clarkkent@gmail.com Password: fair123!

    Grab the access_token from the  browser's url bar and set the token in postman's Bearer-Authorization for the routes below. I've set the tokens to last for 24 hours when project is submitted. 


## Documentation of API behavior and RBAC controls

| REQUEST TYPE | ROUTE | ACCESS PERMISSION | DESCrptn | USER | BODY |
| ------------- | ----- | ------------- | ------------- |------------- | ------------- |
| POST | /studios | post:studios | Adds a studio | Biz OwnerONLY | { bizname:"String", opening_date:"YYYY-MM-DD" } |
| PATCH | /studios/id | patch:studios | Updates a studio |Manager & Biz OwnerONLY | { bizname:"String", opening_date:"YYYY-MM-DD" } |
| GET | /studios | get:studios | Gets list of studios | All LoggedIn Users | N/A |
| GET | /studios/id | get:studios | Get a studio | All LoggedIn Users | N/A |
| DELETE | /studios/id | delete:studios | Delete a studio | Biz OwnerONLY | N/A |
| POST | /instructors | post:instructors | Add an instructor | Manager & Biz OwnerONLY | { name:"String", age:"Number", gender:"String" class_type: "class type" } |
| PATCH | /instructors/id | patch:instructors | Updates an instructor | Manager & Biz OwnerONLY | { name:" String", age:" Number" gender:" String" class_type: "class type"} |
| GET | /instructors | get:instructors | Gets list of instructors| All LoggedIn Users| N/A |
| GET | /instructors/id | get:instructors | Get an instructor | All LoggedIn Users| N/A |
| DELETE | /instructors/id | delete:instructors | delete an instructor | Manager & Biz OwnerONLY | N/A |


## Testing
    ```
    * Locally run test_runner.sh
    * Postman projects - "Virtual Studio Tests.postman_collection.json" is for running the project locally
    * Postman projects - "Virtual Studio Tests Heroku.postman_collection.json" is for running the project is for running the projects on Heroku - which is running.  Replace the JWT tokens as described above. 
    ```







