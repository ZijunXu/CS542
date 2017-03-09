# Backend
- remember to install MongoDB and Start MongoDB
`sudo service mongod start`
- in order to test the item query part you need to import some of the data into the MongoDB which gathered by API module.
- `mongoimport --db test --collection item --drop --file PATH-TO-JSON-FILE` 

### Project current structure
```
.
├── app                          
│   ├── database.py                     # Relational Database
│   ├── forms.py                        # Web forms
│   ├── __init__.py                     # init for the app
│   ├── static                          # folder for static file
│   ├── templates                       # folder for the templates
│   │   ├── index.html
│   │   ├── registration.html
│   │   ├── query.html
│   │   └── test.html
│   └── views.py                        # Control view
├── app.db                              # Relational database
├── config.py                           # Configuration for the app
├── __init__.py                         # init for the server
├── README.md
├── requirements.txt
├── run.py                              # run the server on 5000 port
└── tmp

```
### Current requirements
```
appdirs==1.4.0
click==6.7
Flask==0.12
Flask-Login==0.4.0
Flask-PyMongo==0.4.1
Flask-Script==2.0.5
Flask-SQLAlchemy==2.1
Flask-WTF==0.14.2
itsdangerous==0.24
Jinja2==2.9.5
MarkupSafe==0.23
packaging==16.8
pymongo==3.4.0
pyparsing==2.1.10
requests==2.13.0
six==1.10.0
SQLAlchemy==1.1.5
Werkzeug==0.11.15
WTForms==2.1
```
### ToDo
 - MongoDB
 - Comunication with frontend
