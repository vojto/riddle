# Edit category

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/edit-category/`  
Fields:  
* id - category ID
* name

## Server -> Client
Method: JSON  
Examples:  
* Specified category ID does not exist

  ```json
  {
    "response": "error",
    "reason": "category_not_found"
  }
  ```

* Category edited successfully

  ```json
  {
    "response": "success"
  }
  ```

