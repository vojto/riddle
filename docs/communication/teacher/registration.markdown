# Registration

## Client -> Server
Method: Form POST  
Requires: Nothing  
URL: `/registration/`  
Fields:  
* username
* fullname
* email
* password
* recaptcha_challenge_field
* recaptcha_response_field

## Server -> Client
Method: JSON  
Examples:  
* Incorrect CAPTCHA

  ```json
  {
    "response": "error",
    "reason": "captcha_incorrect"
  }
  ```

* User already exists

  ```json
  {
    "response": "error",
    "reason": "already_exists"
  }
  ```

* Registration successful

  ```json
  {
    "response": "success"
  }
  ```

