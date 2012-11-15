# Login

## Client -> Server
Method: Form POST  
Requires: Nothing  
URL: `/login/`  
Fields:  
* username
* password

## Server -> Client
Method: JSON  
Examples:  
* Wrong username or password

  ```json
  {
    "response": "error",
    "reason": "wrong_password"
  }
  ```

* Login successful

  ```json
  {
    "response": "success"
  }
  ```

