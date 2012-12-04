# Edit questionnaire

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/edit-questionnaire/`  
Fields:  
* id - questonnaire ID
* name (optional)
* category_id (optional)
* public_id (optional)

## Server -> Client
Method: JSON  
Examples:  
* Specified questionnaire ID does not exist

  ```json
  {
    "response": "error",
    "reason": "questionnaire_not_found"
  }
  ```

* Specified category ID does not exist

  ```json
  {
    "response": "error",
    "reason": "category_not_found"
  }
  ```

* Specified public ID already exists

  ```json
  {
    "response": "error",
    "reason": "public_id_already_exists"
  }
  ```

* Questionnaire edited successfully

  ```json
  {
    "response": "success"
  }
  ```

