# Submit question answer

## Client -> Server
Method: Form POST  
Requires: Nothing  
URL: `/submit-question/`  
Fields:  
* question_id
* text_answer OR option_ids

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

* Question requires at least one option

  ```json
  {
    "response": "error",
    "reason": "missing_options"
  }
  ```

* Answer submitted successfully

  ```json
  {
    "response": "success"
  }
  ```

