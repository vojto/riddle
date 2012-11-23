# New questionnaire

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/new-questionnaire/`  
Fields:  
* name
* category_id
* public_id

## Server -> Client
Method: JSON  
Examples:  
* Specified public ID already exists

  ```json
  {
    "response": "error",
    "reason": "already_exists"
  }
  ```

* Specified category ID does not exist

  ```json
  {
    "response": "error",
    "reason": "category_not_found"
  }
  ```

* Questionnaire created successfully

  ```json
  {
    "response": "success"
    "public_id": "8x8rzvIxA0BOnRpw"
  }
  ```

