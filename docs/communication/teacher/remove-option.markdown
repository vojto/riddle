# Remove option

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/remove-option/`  
Fields:  
* option_id

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

* Option removed successfully

  ```json
  {
    "response": "success"
  }
  ```

