# Remove question

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/remove-question/`  
Fields:  
* question_id

## Server -> Client
Method: JSON  
Examples:  
* Specified question ID does not exist

  ```json
  {
    "response": "error",
    "reason": "question_not_found"
  }
  ```

* Question removed successfully

  ```json
  {
    "response": "success"
  }
  ```

