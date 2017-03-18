# Backend
- remember to install MongoDB and Start MongoDB
`sudo service mongod start`
- in order to test the item query part you need to import some of the data into the MongoDB which gathered by API module.
- `mongoimport --db test --collection item --drop --file PATH-TO-JSON-FILE`

### Project current structure
```
.
├── api_server
│   ├── database.py                     # Relational Database
│   ├── forms.py                        # Probably wont use this one anymore
│   ├── __init__.py                     # initialization for the app
│   ├── static                          # Angular.Js
│   │   ├── app-content
│   │   │   └── app.css
│   │   ├── app.js
│   │   ├── app-services
│   │   │   ├── authentication.service.js
│   │   │   ├── flash.service.js
│   │   │   ├── user.service.js
│   │   │   └── user.service.local-storage.js
│   │   ├── home
│   │   │   ├── home.controller.js
│   │   │   └── home.view.html
│   │   ├── index.html
│   │   ├── login
│   │   │   ├── login.controller.js
│   │   │   └── login.view.html
│   │   ├── README.md
│   │   └── register
│   │       ├── register.controller.js
│   │       └── register.view.html
│   └── views.py                        # Control the API
├── app.db                              # Relational database
├── config.py                           # Configuration for the app
├── README.md
├── requirements.txt
├── run.py                              # run the server on 5000 port
└── tmp


```
### Current requirements
```
aniso8601==1.2.0
appdirs==1.4.0
click==6.7
Flask==0.12
Flask-Login==0.4.0
Flask-PyMongo==0.4.1
Flask-RESTful==0.3.5
Flask-Script==2.0.5
Flask-SQLAlchemy==2.1
Flask-WTF==0.14.2
itsdangerous==0.24
Jinja2==2.9.5
MarkupSafe==0.23
packaging==16.8
pymongo==3.4.0
pyparsing==2.1.10
python-dateutil==2.6.0
pytz==2016.10
requests==2.13.0
six==1.10.0
SQLAlchemy==1.1.5
Werkzeug==0.11.15
WTForms==2.1

```
### ToDo
 - MongoDB
 - Comunication with frontend
