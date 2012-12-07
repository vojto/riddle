# List questionnaire comments

## Client -> Server
Method: GET  
Requires: Nothing  
URL: `/list-comments/`  
Fields:  
* qaire_id - questionnaire ID
* offset (optional)

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
    [
      {
        "id": 1,
        "body": "This questionnaire is the best!",
        "subject": "Awesome",
        "datetime": "2012-12-07T01:11:53.467200",
        "author": "John Smith"
      }
      ,
      {
        "id": 2,
        "body": "I am unhappy with this questionnaire.",
        "subject": "Seen better",
        "datetime": "2012-12-07T01:12:00.320045",
        "author": "Nguyen Ngyuen"
      }
  ```

