# Set teacher settings

## Client -> Server
Method: Form POST  
Requires: Nothing  
URL: `/set-teacher-settings/`  
Fields:   
* fullname (optional) - new teacher's full name
* email (optional) - new teacher's email
* old_password (optional) - old teacher's password
* new_password (optional) - new teacher's password

## Server -> Client
Method: JSON  
Examples:  
* Wrong old teacher's password

  ```json
    {
      "response": "error",
      "reason": "wrong_password"
    }
  ```

* Teacher settings saved

  ```json
    {
      "response": "success"
    }
  ```

