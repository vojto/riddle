# Remove questionnaire comment

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/remove-comment/`  
Fields:  
* id: comment ID

## Server -> Client
Method: JSON  
Examples:  
* Specified comment ID does not exist

  ```json
  {
    "response": "error",
    "reason": "comment_not_found"
  }
  ```

* Comment removed successfully

  ```json
  {
    "response": "success"
  }
  ```

