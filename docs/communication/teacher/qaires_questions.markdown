# View questionnaire questions

## Client -> Server
Method: GET  
Requires: Auth  
URL: `/qaires/<qaire_id>/`  
Fields: qaire_id  

## Server -> Client
Method: JSON  
Examples:  
* Typical example

  ```json
      {
        "category": "My first category",
        "name": "How to be polite",
        "questions":
          [
            {
              "type": "text",
              "description": "How are you today?"
              "presented": false
            }
          ]
      }
  ```

