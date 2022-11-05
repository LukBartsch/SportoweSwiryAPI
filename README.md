# Sportowe Świry API

REST API for online library. It supports authors of books and books resources including authentication (JWT Token).

REST API aplikacji Sportowe Świry, która dostępna jest pod adresem [...]. 
Pozwala na dostęp do wszystkich aktywności oraz wydarzeń zapisanych w bazie danych. 
Użytkownik po zalogowaniu może również dodawać i usuwać swoje aktywności sportowe.
Użytkownicy, którzy są administatroami mogą również wyświetlić wszystkich zarejestrowanych użytkoniwków.

REST API for Sportowe Świry application, available at [sportoweswiry.com.pl].
It allows access to all activities and events stored in the database.
After logging in, the user can also add and remove his sports activities.
Admin users can also view all registered users, events or users's activities.

The documentation can be found in `sportowe_swiry_api_documentation.html` or [here](https://documenter.getpostman.com/view/23181522/2s8YYFr3bF)

## Setup

- Clone repository
- Rename .env.example to `.env` and set your values (use the same database like in SportoweSwiry app)
```buildoutcfg
# SQLALCHEMY_DATABASE_URI MySQL template
SQLALCHEMY_DATABASE_URI=mysql+pymysql://<db_user>:<db_password>@<db_host>/<db_name>?charset=utf8mb4
```
- Create a virtual environment
```buildoutcfg
python -m venv venv
```
- Install packages from `requirements.txt`
```buildoutcfg
pip install -r requirements.txt
```
- Run command
```buildoutcfg
flask run
```


**NOTE**



## Tests

In order to execute tests located in `tests/` run the command:

```buildoutcfg
python -m pytest tests/
```

## Technologies / Tools

- Python 3.8.0
- Flask 1.1.2
- Alembic 1.4.2
- SQLAlchemy 1.3.16
- Pytest 5.4.3
- MySQL
- AWS
- Postman