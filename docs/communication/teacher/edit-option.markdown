# Edit option

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/edit-option/`  
Fields:  
* option_id
* text

## Server -> Client
Method: JSON  
Examples:  
* Specified option ID does not exist

  ```json
  {
    "response": "error",
    "reason": "option_not_found"
  }
  ```

* Option edited successfully

  ```json
  {
    "response": "success"
  }
  ```

