## Windows Instructions (PowerShell)



**Virtual Environment Creation and Activation**

In the repository's root directory, create the venv:

`python -m venv venv`

Obtain permission to run the venv activation script:

`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted`

Activate the venv:

`.\venv\Scripts\activate`

Install the requirements

`pip install -r requirements.txt`

**Application Execution**

Run the application

`python .\manage.py runserver`

