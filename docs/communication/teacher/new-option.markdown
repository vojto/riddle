# New option

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/new-option/`  
Fields:  
* question_id
* text

## Server -> Client
Method: JSON  
Examples:  
* Specified question_id does not exist

  ```json
  {
    "response": "error",
    "reason": "question_not_found"
  }
  ```

* Specified question does not support options

  ```json
  {
    "response": "error",
    "reason": "options_not_supported"
  }
  ```

* Option created successfully

  ```json
  {
    "response": "success",
    "option_id": 10
  }
  ```

