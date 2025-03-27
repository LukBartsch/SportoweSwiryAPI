# Sportowe Świry API

REST API for Sportowe Świry application.

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setup](#setup)
* [Tests](#tests)
* [Project Status](#project-status)
* [Contributing](#contributing)
* [Sources](#sources)
* [Contact](#contact)
* [License](#license)


## General Information
The REST API application is a separate module of the Sportowe Świry application (available [here](https://sportoweswiry.com.pl/)) that allows to access the database using the HTTP protocol. The app use a copy of the original application database. This is a module designed to show the functionality of the API.

## Technologies Used
* Framework Python-Flask
* SQLAlchemy
* Pytest
* MySQL
* AWS
* Postman
* Git


## Features
The user, after logging in (JWT Token), has access to all his sports activities and events saved in the database. He can also view, add, delete and update his previous activities. The user can also update his personal data from this application.
Users who are administrators can view all registered users and other data related to them (activities, events).

Data is transmitted and displayed using the JSON format. Displaying a list of activities, events or users can be configured according to your needs. The most important functionalities:

* Authentication between client and server using JWT token (JSON Web Token).
* HTTP methods used: GET, POST, PUT, DELETE.
* Functions for filtering and sorting specific database columns.
* Marshmallow library for serializing, deserializing, and validating data.
* Using pagination when displaying data.

Full documentation can be found [here](https://documenter.getpostman.com/view/23181522/2s8YYFr3bF).

## Setup

* Clone repository
* Rename `.env.example` to `.env` and set your values:
```
SECRET_KEY=SomeRandomString
SQLALCHEMY_DATABASE_URI=mysql+pymysql://<db_user>:<db_password>@<db_host>/<db_name>
```
* Create a virtual environment
```
python -m venv venv
```
* Install packages from `requirements.txt`
```buildoutcfg
pip install -r requirements.txt
```
* Run command
```buildoutcfg
flask run
```

## Tests

In order to execute tests located in `tests/` run the command:

```
python -m pytest tests/
```

## Project Status

The project is now complete. No additional work is planned.
The application was deployed on the AWS cloud using the Elastic Beanstalk service. The application used an EC2 server and an S3 container in the Free Tier version. The implementation was made for educational purposes only.

## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

Fork the Project
* Create your Feature Branch (git checkout -b feature/AmazingFeature)
* Commit your Changes (git commit -m 'Add some AmazingFeature')
* Push to the Branch (git push origin feature/AmazingFeature)
* Open a Pull Request

## Sources
This project was based on [this tutorial.](https://www.udemy.com/course/rest-api-krok-po-kroku-python-flask-mysql/)

## Contact
Created by [@LukBartsch](https://github.com/LukBartsch) - feel free to contact me!

[![LinkedIn][github-shield]][github-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


## License
This project is open source and available under the MIT License.


[github-shield]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
[github-url]: https://github.com/LukBartsch
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/lukasz-bartsch/
