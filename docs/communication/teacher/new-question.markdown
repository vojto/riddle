# Edit question

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/new-question/`  
Fields:  
* description (optional)
* typ (optional)
* presented (optional)
* public_id (optional)

## Server -> Client
Method: JSON  
Examples:  
* Specified public ID does not exist

  ```json
  {
    "response": "error",
    "reason": "public_id_not_found"
  }
  ```

* Wrong question type specified

  ```json
  {
    "response": "error",
    "reason": "unknown_question_type"
  }
  ```

* Question created successfully

  ```json
  {
    "response": "success",
    "question_id": 8
  }
  ```

