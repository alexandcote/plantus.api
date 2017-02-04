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
  
3. Add some config to your .bash_profile or .zshrc
  ```
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
  ```

4. Be sure to have the last version of xcode
  ```
  xcode-select --install
  ```

5. Install python good python version
  ```
  pyenv install 3.5.3
  ````

6. Create a virtualenv for the project
  ```
  pyenv virtualenv 3.5.3 plantus
  ```

7. Install PostgreSQL
  ```
  brew install postgres
  ```
  
8. Start the postgresql server
  ```
  brew services start postgresql
  ```

9. Create the database
  ```
  createdb plantus_development
  ```
  
10. Create the user
  ```
  createuser -s plantus
  ```

11. Clone this repository
  ```
  git clone git@github.com:alexandcote/plantus.api.git
  ```

12. Create a file in the root of the project
  ```
  cd plantus.api
  echo 'plantus' >> .python-version
  ```

13. In the project directory, install the dependencies
  ```
  pip install -r requirements-test.txt
  ```
  
14. Copy the .env file
  ```
  cp .env.development .env
  ``` 

15. Do the migration of the database
  ```
  ./manage.py migrate
  ```

16. Load default fixtures
  ```
  ./manage.py loaddata ./**/fixtures/*.json
  ```

17. Run the server
  ```
  ./manage.py runserver
  ```
