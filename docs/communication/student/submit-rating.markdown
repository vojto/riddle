# Submit questionnaire rating

## Client -> Server
Method: Form POST  
Requires: Nothing  
URL: `/submit-rating/`  
Fields:  
* qaire_id - questionnaire ID
* like - "1" ("true") or "0" ("false")

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

* Student already rated this questionnaire

  ```json
  {
    "response": "error",
    "reason": "already_rated"
  }
  ```

* Rating submitted successfully

  ```json
  {
    "response": "success"
  }
  ```

