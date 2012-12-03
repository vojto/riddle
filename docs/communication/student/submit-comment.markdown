# Submit comment

## Client -> Server
Method: Form POST  
Requires: Nothing  
URL: `/submit-comment/`  
Fields:  
* qaire_id
* subject
* body

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

* Comment submitted successfully

  ```json
  {
    "response": "success"
  }
  ```

