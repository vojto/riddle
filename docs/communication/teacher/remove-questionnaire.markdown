# Remove questionnaire and its questions

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/remove-questionnaire/`  
Fields:  
* public_id

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

* Questionnaire removed successfully

  ```json
  {
    "response": "success"
  }
  ```

