![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white) ![cypress](https://img.shields.io/badge/-cypress-%23E5E5E5?style=for-the-badge&logo=cypress&logoColor=058a5e) ![CircleCI](https://img.shields.io/badge/circle%20ci-%23161616.svg?style=for-the-badge&logo=circleci&logoColor=white)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/uno-isqa-8950/uno-cpi/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/uno-isqa-8950/uno-cpi/tree/master)

UNO CPI
UNO Community Partnership Intiative

The official repository of the Community Engagement Partnership Initiative (UNO) Project for the Spring 2023 Capstone classes at the University of Nebraska at Omaha Written in Python/Django

    •	PostgresSQL Version 14

    •	Heroku Stack 22

    •	CircleCi Version 2.1

    •	Cypress Version 13.6.6

Highlights

|    Functionality     |         Related packages         |                                                                                                                                                                                                                                            Versions                                                                                                                                                                                                                                             |
| :------------------: | :------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| Programming Language |              Python              |                                                                                                                                                                                   [![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31010/)                                                                                                                                                                                   |
|      Framework       |              Django              |                                                                                                                                                                                            [![Django 5.2](https://img.shields.io/badge/django%20-5.2-blue)](https://www.djangoproject.com/download/)                                                                                                                                                                                            |
|    Single Sign On    | SAML, xmlsec, isodate, six, lxml | [![python3-saml](https://img.shields.io/badge/python3--saml-1.16.0-blue)](https://pypi.org/project/python3-saml/) [![xmlsec](https://img.shields.io/badge/xmlsec-1.3.13-blue)](https://pypi.org/project/xmlsec/) [![isodate](https://img.shields.io/badge/isodate-0.7.2-blue)](https://pypi.org/project/isodate/) [![six](https://img.shields.io/badge/six-1.11.0-blue)](https://pypi.org/project/six/) [![lxml](https://img.shields.io/badge/lxml-4.9.2-blue)](https://pypi.org/project/lxml/) |
| Data import / Export | django-import-export, XlsWriter  |                                                                                                                        [![django-import-export](https://img.shields.io/badge/django--import--export-4.3.7-blue)](https://pypi.org/project/django-import-export/) [![xlswriter](https://img.shields.io/badge/XlsWriter-3.2.2-blue)](https://pypi.org/project/XlsxWriter/)                                                                                                                        |
|         CMS          |             Wagtail              |                                                                                                                                                                                                [![wagtail](https://img.shields.io/badge/wagtail-6.4.1-blue)](https://pypi.org/project/wagtail/)                                                                                                                                                                                                 |
|  Automated Testing   |            npx, node             |                                                                                                                      [![npx](https://img.shields.io/badge/npx-9.5.0-blue)](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) [![node](https://img.shields.io/badge/node-19.7.0-blue)](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)                                                                                                                       |

Getting Started:

Install Python 3.10 from https://www.python.org/downloads/

```
    pip install -r requirements.txt
```

Database Migration:

Navigate to the folder containing manage.py and run the following commands in order.

```
    python manage.py makemigrations

    python manage.py migrate

    python manage.py runserver
```

Test Server:

Navigate to the folder containing manage.py and run the following command.

    python manage.py runserver

navigate to http://127.0.0.1:8000/ to go to the home page.
