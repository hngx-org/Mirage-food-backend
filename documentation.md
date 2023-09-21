
## Documentation for All API Endpoints In the Organization App

 ### Get an Organization

### Endpoint

 `URL:   users/<int:user_id>/organizations/<int:org_id>`
 
 Method: GET
 
#### Description:
-   Use this endpoint to retrieve the organization associated with a specific user. It takes two parameters , org_id to identify the organisation and user_id to identify the user.The org_id must be associated with the user_id in order to get the organization. Invalid parameters will result to errors.
#### Parameters:

    -   `user_id` (int): The primary key (ID) of the user for whom you want to retrieve the organization.
    -   `org_id` (int): The primary key (ID) of the organization you want to retrieve.


### Example Usage
**Request**
*Example Get request*

`GET /api/organization/879/34/`

*Example response(success)*
```
HTTP/1.1  200 OK 
Content-Type: application/json 
{  "id":  34, 
 "name":  "Example Organization",  
 "description":  "A sample organization", ... }
```
 **Error responses:**
- Organization Not Found:
- Content-Type: application/json
```
status: status.HTTP_404_NOT_FOUND
{'error': 'Organization not found for this user'}
```
- User Not Found
- Content-Type: application/json
```
 status: status.HTTP_404_NOT_FOUND
{'error': 'User not found for this user'}
```

### Update an organization
### Endpoint

   `URL:   organization/<int:pk>/`
 
 Method: PUT | PATCH

#### Description:
This API endpoint provides functionality for updating organization resources using HTTP PUT and PATCH methods. It takes one parameter which the ID of the organization.  
#### Parameters:     
  `<int:pk>:  The primary key (ID) of the organization you want to update.`

### Example Usage
**Request**
 *Request Headers*
 `Content-Type` (header): `application/json`
 
 *Request Body*
 `application/json` for JSON data.

*Example PUT  request*
```
PUT /api/organization/34/`or
Content-Type: application/json
{
 "organisation_name":  "Example Organization", 
 "lunch_price":"upto date lunch price",
 "currency":"example ksh"
 }
 ```
 *Example PATCH request*
```
`PATCH /api/organization/34/`

Content-Type: application/json
{ 
"lunch_price": "Updated organization lunch price" 
}
```
**Example response(success)**

*organization updated successfully*

status: status.HTTP_200_OK

 **Example Error responses:**
 
*Bad request or invalid data:*
- Content-Type: application/json
```
HTTP/1.1  400 Bad Request
 Content-Type: application/json
  { 
   "errors": 
    [  "Field 'organisation_name' is required.", 
     "Field 'currency' must be a string."  
     ] 
  }
```
*Resource Not Found*
```
`HTTP/1.1 404 Not Found
Content-Type: application/json

{
    "error": "organisation not found."
}
```


### Create an Organization

### Endpoint

 `URL:  /api/organization/create`
 
 Method: PUT
#### Description:
When the user is created,  a lunch price is assigned to the organization table along with the org_id field. The user has to be loggedIn in order to create an organization. After successfully logging in, the access is token returned back. The access token would then be used to update the organization name ,lunch price and currency on the table.
 #### Parameters :   None
 
###  Example usage
*Request Headers:*
 `Authorization: Bearer <access_token>`
 
*Request Body:*
`Content-Type: application/json`
       
  *Example PUT  request*
```
PUT /api/organization/create`
Content-Type: application/json
   {
        "name": "example organisation",
        "lunch_price": "" // default to "#1000" if not set
        "currency":"currency detail"  
  }
```
**Example response(success)**

*organization created successfully*

status: status.HTTP_201_CREATED
```
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/resource/35/

{
    "id": 35,
    "name": "New organization Name",
    "lunch_price": "Detail of lunch price",
    "currency":"currency detail"
    
}
```

 **Example Error responses:**

*authentication failure*
- Content-Type: application/json
```
HTTP/1.1  401 Unauthorized

  { 
   "error": Authentication failed.",  
  }
```

*Forbidden*
- Content-Type: application/json
```
HTTP/1.1  403 Forbidden

  { 
   "error": User not authorized to create an organization.",  
  }
```
*Bad request or invalid data:*
- Content-Type: application/json
```
HTTP/1.1  400 Bad Request
 Content-Type: application/json
  { 
   "errors": 
    [  "Field 'name' is required.", 
     "Field 'currency' must be a string."  
     ] 
  }
```

  ### Create Organization Invite (Admin Only)
  
  ###  Endpoint: 
  URL:  `/api/organization/invite`
  
   Method: `POST`
   #### Description
   This endpoint allows an admin user to send an invitation to users to join an organization
  #### Parameters: None

 
###  Example usage
*Request Headers:*
 `Authorization: Bearer <access_token>`
 
*Request Body:*
`Content-Type: application/json`
       
  *Example POST  request*
```
POST /api/organization/invite
Content-Type: application/json

{ 
     "email": "kurves@orglunch.com"
 }
```
**Example response(success)**

*organization invite created successfully*

status: status.HTTP_201_CREATED
*Response Body*
```
{ 
"message": "success", 
"statusCode": 200, 
"data": null 
}
```
 **Example Error responses:**
 
*Bad request or invalid data*
- Content-Type: application/json
```
HTTP/1.1  400 Bad Request
 Content-Type: application/json
  { 
   "error": "Field 'email' must be a string.", 
  }
```
*authentication failure*
- Content-Type: application/json
```
HTTP/1.1  401 Unauthorized

  { 
   "error": Authentication failed.",  
  }
```

*Forbidden*
- Content-Type: application/json
```
HTTP/1.1  403 Forbidden

  { 
   "error": User not authorized to create an organization invite.",  
  }
```

