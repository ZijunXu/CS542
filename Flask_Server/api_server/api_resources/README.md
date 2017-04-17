# API Usage

- ## UserLogin
    - route: /api/authenticate
    - method: POST
    - Description: Since it is POST method, we need to submit a form while calling this api
    - Example:
    ```bash
    # Failed, without a form
    curl -i http://localhost:5000/api/authenticate     
    HTTP/1.0 405 METHOD NOT ALLOWED
    Content-Type: application/json
    Content-Length: 70
    Allow: OPTIONS, POST
    Server: Werkzeug/0.11.15 Python/3.5.2
    Date: Thu, 13 Apr 2017 13:12:37 GMT

    {
    "message": "The method is not allowed for the requested URL."
    }

    # Success with a form that satifsy the need
    curl -i -H "Content-Type: application/json" -X POST -d '{"username":"a","password":"a"}' http://localhost:5000/api/authenticate
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 165
    Server: Werkzeug/0.11.15 Python/3.5.2
    Date: Thu, 13 Apr 2017 13:15:14 GMT

    {
      "login_status": true,
      "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ5MjA4OTkxNCwiaWF0IjoxNDkyMDg5MzE0fQ.eyJpZCI6MX0.oG44hWSx9nZi0UcyRUycwS2_WmI2xYgr-gRfsWWvIfg"
    }

    ```
- ## UserRegister
  - route: /api/reg
  - method: POST
  - Description: Since it is POST method, we need to submit a form while calling this api
  - Example:

  ```bash
  # Failed
  curl -i http://localhost:5000/api/reg     
  HTTP/1.0 405 METHOD NOT ALLOWED
  Content-Type: application/json
  Content-Length: 70
  Allow: OPTIONS, POST
  Server: Werkzeug/0.11.15 Python/3.5.2
  Date: Thu, 13 Apr 2017 13:12:37 GMT

  {
  "message": "The method is not allowed for the requested URL."
  }
  # Success
  curl -i -H "Content-Type: application/json" -X POST -d '{"username":"test","password":"test","email":"tset@test.com","confirm_password":"test","accept_tos":"true"}' http://localhost:5000/api/reg
  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 30
  Server: Werkzeug/0.11.15 Python/3.5.2
  Date: Thu, 13 Apr 2017 13:22:29 GMT

  {
    "register_status": true
  }
  ```


- ## UserItemSearchHistory
  - route: /api/user/search, /api/user/search/<sid>
  - method: GET, DELETE, all of them required as a login user
  - Description:
    - GET:

      ```bash
      curl -H "Authorization: Bearer eyJpYXQiOjE0OTI0NjE3NTIsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDkyNDYyMzUyfQ.eyJpZCI6MX0.qRxQ3G6otiZinXvZeh3REAafW4a780AkT93WqXvsp64" -i http://localhost:5000/api/user/search
      HTTP/1.0 200 OK
      Content-Type: application/json
      Content-Length: 207
      Server: Werkzeug/0.11.15 Python/3.5.2
      Date: Mon, 17 Apr 2017 20:36:23 GMT

      [
        {
          "id": 1,
          "item": "NB",
          "sid": 1,
          "time": "Sun, 09 Apr 2017 17:31:03 GMT"
        },
        {
          "id": 1,
          "item": "NB1",
          "sid": 2,
          "time": "Sun, 09 Apr 2017 17:31:03 GMT"
        }
      ]
      ```

    - DELETE: Deleting a users search history record, request token for user specification

      ```bash
      curl  -H "Authorization: Bearer eyJpYXQiOjE0OTI0NjE3NTIsImFsZyI6IkhTMjU2IiwiZXhwIjoxNDkyNDYyMzUyfQ.eyJpZCI6MX0.qRxQ3G6otiZinXvZeh3REAafW4a780AkT93WqXvsp64" -X delete  http://localhost:5000/api/user/search/2
      {
        "delete_history_status": "Success"
      }
      ```

- ## UserCurrencyPostManagement
  - route: /api/user/post, /api/user/post/<tid>
  - method: POST, GET, DELETE


- ## Admin
  - route: /api/admin/
  - method: POST, GET, DELETE
  - Description:
    - GET: this method is temporarily for test, return all of the user
      ```bash
      curl -i http://localhost:5000/api/admin
      HTTP/1.0 200 OK
      Content-Type: application/json
      Content-Length: 482
      Server: Werkzeug/0.11.15 Python/3.5.2
      Date: Thu, 13 Apr 2017 14:23:36 GMT

      [
        {
          "email": "a@a.com",
          "id": 1,
          "name": "a",
          "password_hash": "pbkdf2:sha1:1000$bO9dxNFj$5d4c56816c414043ce534bdc7c7deef5dd111224"
        },
        {
          "email": "b@b.com",
          "id": 2,
          "name": "b",
          "password_hash": "pbkdf2:sha1:1000$w7ChHq3w$b007fe0b0805f1e124419b903374ddcfe2469893"
        },
        {
          "email": "tset@test.com",
          "id": 3,
          "name": "test",
          "password_hash": "pbkdf2:sha1:1000$XFnZVd01$878f05ed0072f5efcf99c9e681d18ee8b6faaa6e"
        }
      ]
      ```

    - POST: create a new user

      ```bash
      curl -i -H "Content-Type: application/json" -X POST -d '{"username":"test1","password":"test1","email":"tset1@test.com","confirm_password":"test1","accept_tos":"true"}' http://localhost:5000/api/admin
      host:5000/api/admin
      HTTP/1.0 200 OK
      Content-Type: application/json
      Content-Length: 30
      Server: Werkzeug/0.11.15 Python/3.5.2
      Date: Thu, 13 Apr 2017 14:26:15 GMT

      {
        "register_status": true
      }
      ```

    - DELETE: Deleting a users search history record, request token for user specification

      ```bash
      curl -X delete  http://localhost:5000/api/admin/test1
      {
        "delete_status": "Success"
      }
      ```

- ## UserCurrencyPostSearch
  - route: /api/currency/<currency_name>, /api/currency
  - method: POST, GET
  - Description:
    - GET: this only a temporary method for testing, this return all of the currency

    ```bash
    curl -i http://localhost:5000/api/currency
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 48
    Server: Werkzeug/0.11.15 Python/3.5.2
    Date: Thu, 13 Apr 2017 14:41:32 GMT

    [
     {
       "cid": 1,
       "cname": "Wings"
     }
    ]
    ```

    - POST: request a form contain the currency name, this method will return all the post related to this currency

    ```bash
    curl -i -H "Content-Type: application/json" -X POST -d '{"currency_name":"NB"}' http://localhost:5000/api/currency
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 173
    Server: Werkzeug/0.11.15 Python/3.5.2
    Date: Thu, 13 Apr 2017 14:45:16 GMT

    [
      {
        "c1_item": "NB",
        "c1_number": 1,
        "c2_item": "LGD",
        "c2_number": 2,
        "tid": 1,
        "time": "Sun, 09 Apr 2017 17:31:03 GMT",
        "uid": 1
      }
    ]
    ```

- ## UserInfoUpdate
- route: /api/update
- method: PUT
- Description:
  - PUT:

  ```bash
  curl -i -H "Content-Type: application/json" -X PUT -d '{"username":"test","password":"test1","email":"tset1@test.com","confirm_password":"test1"}' http://localhost:5000/api/user/update
  HTTP/1.0 200 OK
  Content-Type: application/json
  Content-Length: 28
  Server: Werkzeug/0.11.15 Python/3.5.2
  Date: Thu, 13 Apr 2017 14:59:13 GMT

  {
    "update_status": true
  }
  ```


- ## GetToken
  - route: /api/token
  - method: GET
  - Description: This api only support GET, not done yet

- ## mongoQuery
  - route: /api/item
  - method: POST
  - Description: This api only support POST, not done yet
