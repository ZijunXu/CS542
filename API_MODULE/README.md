# Crawler

### structure
```
.
├── data
│   └──                           # Place to store the json data
├── last_user.json                # File to record the Crawler's next API parameter
├── poe_api.py                    # The Crawler
└── README.md
```
### Current requirements
```
requests==2.13.0
```
### Usage
```
a = get_data_api()
a.get_api_response()
# then repeat the method get_api_response() you can get the data
# a lot can be done here
```
### To Do
- Store the data into the MongoDB
