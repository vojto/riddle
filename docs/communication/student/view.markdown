# View questionnaires

## Client -> Server
Method: GET
Requires: Auth
URL: `/view/<qaire_id>/`
Fields:
* qaire_id - questionnaire id

## Server -> Client
Method: JSON
Examples:
* Typical example

  ```json
    {
      "name": "Death Metal",
      "category": "Music",
      "questions":
        [
          {
            "type": "single",
            "description": "Do you like death metal?",
            "options":
              [
                {
                  "text": "Yes."
                }
                ,
                {
                  "text": "Absolutely!"
                }
              ]
          }
          ,
          {
            "type": "multi",
            "description": "What are common lyrical themes in death metal?",
            "options":
              [
                {
                  "text": "death"
                }
                ,
                {
                  "text": "gore"
                }
                ,
                {
                  "text": "flowers"
                }
              ]
          }
          ,
          {
            "type": "text",
            "description": "Tell me something about your childhood."
          }
        ]
    }
  ```

