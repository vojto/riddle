# View questionnaires

## Client -> Server
Method: GET
Requires: Auth
URL: `/qaire/`
Fields: None

## Server -> Client
Method: JSON
Examples:
* Typical example

  ```json
    [
      {
        "category": "Biology",
        "questionnaires":
          [
            {
              "name": "1st lesson (Coleoptera)",
              "public_id": "coleoptera"
            }
            ,
            {
              "name": "2nd lesson (Canidae)",
              "public_id": "canidae"
            }
          ]
      }
      ,
      {
        "category": "Mathematics",
        "questionnaires":
          [
            {
              "name": "1st lesson (Natural numbers)",
              "public_id": "naturalnumbers"
            }
            ,
            {
              "name": "2nd lesson (Real numbers)",
              "public_id": "realnumbers"
            }
          ]
      }
    ]
  ```

