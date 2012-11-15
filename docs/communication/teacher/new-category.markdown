# New category

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/new-category/`  
Fields:  
* name

## Server -> Client
Method: JSON  
Examples:  
* Category already exists

  ```json
  {
    "response": "error",
    "reason": "already_exists"
  }
  ```

* Category created successfully

  ```json
  {
    "response": "success"
  }
  ```

