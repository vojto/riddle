# View option results

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/results-options/`  
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

* Specified question type is not 'single' or 'multi'

  ```json
  {
    "response": "error",
    "reason": "wrong_question_type"
  }
  ```

* Typical example

  ```json
    {
      "question_answers":
        [
          {
            "option_id": "10",
            "option_text": "Yes",
            "count": "1200"
          }
          ,
          {
            "option_id": "11",
            "option_text": "No",
            "count": "2500"
          }
        ],
      "question_type": "text"
    }
  ```

