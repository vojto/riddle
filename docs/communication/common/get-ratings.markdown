# Get questionnaire ratings

## Client -> Server
Method: GET  
Requires: Nothing  
URL: `/get-ratings/`  
Fields:  
* qaire_id - questionnaire ID

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

* Typical example

  ```json
    {
      "likes": 1200,
      "dislikes": 2400
    }
  ```

