# Edit question

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/edit-question/`  
Fields:  
* id - question ID
* description (optional)
* typ (optional)
* presented (optional)
* public_id (optional)

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

* Question edited successfully

  ```json
  {
    "response": "success"
  }
  ```

