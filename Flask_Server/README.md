# Backend
- remember to install MongoDB and Start MongoDB
`sudo service mongod start`
- in order to test the item query part you need to import some of the data into the MongoDB which gathered by API module.
- `mongoimport --db test --collection item --drop --file PATH-TO-JSON-FILE`

### Introduction to the REST
 > this part is from Flask Web Development
- Client-Server: There must be a clear separation between the clients and the server
- Stateless: A client request must contain all the information that is necessary to carry it out. The server must not store any state about the client that persists from one requests to another.
- Cache: Responses from the server can be labeled as cacheable or noncacheable so that clients(or intermediaries between clients and servers) can use a cache for optimization purposes.
- Uniform Interface: The protocol by which clients access server resources must be consistent, well defined, and standardized. The commonly used uniform interface of REST web services is the HTTP protocol.
- Layered System: Proxy servers, caches, or gateways can be inserted between clients and servers as necessary to improve performance, reliability, and scalability
- Code on demand: Client can optionally download code from the server to execute in their context.

### Project current structure
```
.
├── api_server
│   ├── database.py                      # Relational Database
│   ├── forms.py
│   ├── __init__.py                      # initialization for the app
│   ├── mongoQuery.py
│   ├── static                           # Angular.Js
│   │   ├── app-content
│   │   │   ├── app.css
│   │   │   └── item.main.css
│   │   ├── app.js
│   │   ├── app-services
│   │   │   ├── authentication.service.js
│   │   │   ├── currency_result.service.js
│   │   │   ├── flash.service.js
│   │   │   ├── item_result.service.js
│   │   │   ├── search.service.js
│   │   │   └── user.service.js
│   │   ├── currency
│   │   │   ├── currency_post.controller.js
│   │   │   ├── currency_post.view.html
│   │   │   ├── currency_result.controller.js
│   │   │   ├── currency_result.view.html
│   │   │   ├── currency_search.controller.js
│   │   │   └── currency_search.view.html
│   │   ├── home
│   │   │   ├── home.controller.js
│   │   │   └── home.view.html
│   │   ├── index.html
│   │   ├── item
│   │   │   ├── history.controller.js
│   │   │   ├── history.view.html
│   │   │   ├── item_result.controller.js
│   │   │   ├── item_result.view.html
│   │   │   ├── item_search.controller.js
│   │   │   └── item_search.view.html
│   │   ├── login
│   │   │   ├── login.controller.js
│   │   │   └── login.view.html
│   │   ├── README.md
│   │   └── register
│   │       ├── register.controller.js
│   │       └── register.view.html
│   └── views.py
├── app.db                             # database
├── config.py                          # configuration for the server
├── README.md
├── requirements.txt
└── run.py                             # run the server on 5000 port


```
### Current requirements
```
aniso8601==1.2.0
appdirs==1.4.0
cffi==1.9.1
click==6.7
cryptography==1.7.2
Flask==0.12
Flask-HTTPAuth==3.2.2
Flask-PyMongo==0.4.1
Flask-RESTful==0.3.5
Flask-Script==2.0.5
Flask-SQLAlchemy==2.1
Flask-WTF==0.14.2
idna==2.5
itsdangerous==0.24
Jinja2==2.9.5
MarkupSafe==0.23
packaging==16.8
pyasn1==0.2.3
pycparser==2.17
PyJWT==1.4.2
pymongo==3.4.0
pyparsing==2.1.10
python-dateutil==2.6.0
pytz==2016.10
requests==2.13.0
six==1.10.0
SQLAlchemy==1.1.5
Werkzeug==0.11.15
WTForms==2.1
WTForms-JSON==0.3.1

```
### ToDo
 - MongoDB
 - Comunication with frontend
