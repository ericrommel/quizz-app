# A Quiz App
###### source: Exponential Ventures
[![Build Status](https://travis-ci.com/ericrommel/quizz-app.svg?branch=master)](https://travis-ci.com/github/ericrommel/quizz-app)
[![codecov](https://codecov.io/gh/ericrommel/quizz-app/branch/master/graph/badge.svg)](https://codecov.io/gh/ericrommel/quizz-app)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


Nowadays, it has become popular amongst internet users to spend some of their time
testing their general knowledge through quizzes (and brag about it when they ace it). The idea
is to design the prototype for a quiz app that is pleasant, engaging, and easy to use. In the end,
we’ll inform the user about his performance and translate those results into a grade.


## Project Requirements

1. Each question has only four possible answers, of which only one is correct.
2. On top of showing the grade, show statistics on how the user’s answers compared to the
other users that answered these questions before
3. On the results page, show a range of different expertise levels for each grade bracket
with a short description for each expertise level. E.g.
- Score 0-2: Clueless. Don’t be discouraged! Learn some more about this topic,
and come back to try again!
- Score 3-5: Beginner. This is the level most players end up with after answering
this quiz for the first time. Learn some more about this topic and come back to try
again!
- core 5-8: Confident: This is the level players are getting pro! Continue your
progress and rock it!
- Score 8-10: Expert: This is the highest level achievable! Thanks for being
awesome as you are!
4. Show the time it took to answer the quiz.
5. We encourage you to work with your creativity, implementing features and quizzes that
you would like to see and answer
6. Create an authentication method, and only allow users who were already registered in
the database, so you will not need to create a signup page.

#### Bonus Features

1. Allow the user to share the result of his quiz on social media.
2. Allow multiple quizzes to be administered through the same app.
3. Record the user’s performance from previous attempts and compare performance
improvement over time.
4. Sign up page for new users.
5. Testing coverage - Testing is highly encouraged as a bonus feature


## Technical Requirements

These are the main tech requirement. The complete list is in requirements.txt.
- [Python 3](http://python.org/)
- [Pip](https://pip.pypa.io/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLite](http://sqlite.org/) (or any other supported database)

These are optional but recommended.

- [Black](http://black.readthedocs.io/)
- [Codecov](http://codecov.io/)
- [Flake8](http://flake8.pycqa.org/)
- [Pipenv](http://pipenv.readthedocs.io)
- [Pre-commit](http://pre-commit.com/)


### Installing

The default Git version is the master branch. ::

    # clone the repository
    $ cd desired/path/
    $ git clone git@github.com:ericrommel/quizz-app.git/

The next step is install the project's Python dependencies. Just like _Git_ if you still don't have it go to the [official site](http://python.org/) and get it done. You'll also need [Pip](https://pip.pypa.io/), same rules applies here. Another interesting tool that is not required but strongly recommended is [Pipenv](http://pipenv.readthedocs.io), it helps to manage dependencies and virtual environments.

Installing with **Pip**:

    $ cd path/to/quiz-project
    $ pip install -r requirements.txt

Installing with **Pipenv**:

    $ pip install --upgrade pipenv
    $ cd path/to/quiz-project
    $ pipenv sync -d

### Start Container

Docker and docker-compose should be installed first. [Tutorial here](https://docs.docker.com/install/).
At the repo root run:
    $ docker-compose up --build

Now you can use. Open http://127.0.0.1:5000 in a browser and enjoy!


### Run
If you want to run without docker, configure the application manually. This will require you to define a few variables and create the database.

Note: The pipenv virtual environment should be done.

Set the environment variables::

    $ export FLASK_APP=backend/run
    $ export FLASK_ENV=development
    $ export FLASK_CONFIG=development

Or on Windows cmd::
    > set FLASK_APP=src
    > set FLASK_ENV=development
    > set FLASK_CONFIG=development

Create the database::

    $ flask db init
    $ flask db migrate
    $ flask db upgrade

Run the application::

    $ flask run

Open http://127.0.0.1:5000 in a browser.

Note: An *ADMIN* user should be add first. After that, you can add questions. Check the next section for more details.

### Tests
In order to support the manual and automated tests, two requests were create to help using [Postman](https://www.postman.com/).
Feel free to use any other tool for API testing.
1. Add admin user  # It will add a user that can add questions
2. Add questions in bulk  # It will populate the database with questions

From Postman::
- Import the collection file: postman/
- Import the environment file: postman/

Note: You can see the sample file to add questions in the [static folder](https://github.com/ericrommel/quizz-app/blob/master/backend/src/static/sample_questions.xlsx). This template should be used to add questions by this request.

From Python code tests (unit tests)::

    $ pytest

Run with coverage report::

    $ coverage run -m pytest
    $ coverage report
    $ coverage html  # open htmlcov/index.html in a browser

### Kubernetes (K8s)

The project is running on Google Cloud after k8s settings. You can check the project on the Internet accessing the link
below in your browser:

    http://35.205.34.26/

The file quizz-app.yml contains the settings used.


## About

This project is part of [Exponential Ventures'](http://www.exponentialventures.com) challenge for their Full-Stack
hire process sent in November 2020. The whole project includes to create the front-end part using React.

## Author

- [Eric Dantas](https://github.com/ericrommel)

## License

This project is licensed under the GNU License - see the [License](./LICENSE) file for details.
