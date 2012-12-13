# View text results

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/results-texts/`  
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

* Specified question type is not 'text'

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
            "text": "10 years",
            "student": "Anonymous"
          }
          ,
          {
            "text": "3700 days",
            "student": "KillerNoMercy"
          }
        ],
      "question_type": "text"
    }
  ```

