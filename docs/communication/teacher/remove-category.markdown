# Remove category

## Client -> Server
Method: Form POST  
Requires: Auth  
URL: `/remove-category/`  
Fields:  
* id - category ID

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

* Category removed successfully

  ```json
  {
    "response": "success"
  }
  ```

