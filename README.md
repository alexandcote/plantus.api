# Plantus.Api
[![CircleCI](https://circleci.com/gh/alexandcote/plantus.api.svg?style=svg&circle-token=dfb820b713279d7c2946591109dacad84eee61c8)](https://circleci.com/gh/alexandcote/plantus.api)

1. Install [pyenv](https://github.com/yyuu/pyenv)
  ```
  brew update
  brew install pyenv
  ```

2. Install [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv)
  ```
  brew install pyenv-virtualenv
  ```

3. Install python good python version
  ```
  pyenv install 3.5.3
  ````

4. Create a virtualenv for the project
  ```
  pyenv virtualenv 3.5.2 plantus
  ```

5. Install PostgreSQL
  ```
  brew install postgres
  ```

6. Create the database
  ```
  createdb plantus_development
  ```
  
6. Create the user
  ```
  createuser -s plantus
  ```

7. Clone this repository
  ```
  git clone git@github.com:alexandcote/plantus.api.git
  ```

5. Create a file in the root of the project
  ```
  cd plantus.api
  echo 'plantus' >> .python-version
  ```

8. In the project directory, install the dependencies
  ```
  pip install -r requirements-test.txt
  ```

9. Do the migration of the database
  ```
  python manage.py migrate
  ```

10. Run the server
  ```
  python manage.py runserver
  ```
