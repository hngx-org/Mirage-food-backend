# Free Lunch API Documentation

This document provides information about the Free Lunch API, which is designed to handle the backend of the Free Lunch application. The API allows users to perform various actions related to user management, organization management, lunch transactions, and withdrawals. The API is based on the Swagger 2.0 specification.

## Table of Contents

1. [General Information](#general-information)

   - [Base URL](#base-url)
   - [Authentication](#authentication)

2. [Endpoints](#endpoints)

   - [User Signup](#user-signup)
   - [Create an Organization](#create-an-organization)
   - [Create Organization Invite (Admin Only)](#create-organization-invite-admin-only)
   - [Create Organization Wallet](#create-organization-wallet)
   - [Get Organization Balance](#get-organization-balance)
   - [List All Lunches](#list-all-lunches)
   - [Send a Lunch](#send-a-lunch)
   - [Delete a Lunch](#delete-a-lunch)
   - [Search for a User](#search-for-a-user)
   - [List All Users](#list-all-users)
   - [User Login](#user-login)
   - [Get User Details](#get-user-details)
   - [Delete User](#delete-user)
   - [Get User's Lunch](#get-users-lunch)
   - [Get User's Organization](#get-users-organization)
   - [Request a Withdrawal](#request-a-withdrawal)
   - [Get Withdrawal Details](#get-withdrawal-details)
   - [Update Withdrawal](#update-withdrawal)

3. [Definitions](#definitions)
   - [UserRegistration](#userregistration)
   - [OrganizationLunchWallet](#organizationlunchwallet)
   - [Lunch](#lunch)
   - [ListInvites](#listinvites)
   - [Organization](#organization)
   - [UserList](#userlist)
   - [WithdrawalRequest](#withdrawalrequest)
   - [Withdrawal](#withdrawal)

## General Information

### Base URL

The base URL for all API endpoints is `your_url/api`.

### Authentication

The API uses Basic Authentication. You need to include your username and password with each request to authenticate.

## Endpoints

### User Signup

- **Endpoint**: `/auth/user/signup/`
- **HTTP Method**: POST
- **Description**: Create a new user account.
- **Parameters**:
  - `data` (in body, required) - User registration data. See [UserRegistration](#userregistration) for details.
- **Responses**:
  - `201` - User account created successfully. Response schema: [UserRegistration](#userregistration)
- **Tags**: auth

### Create an Organization

- **Endpoint**: `/api/organization/create`
- **Method**: PUT
- **Description**: When the user is created, a lunch price is assigned to the organization table along with the org_id field. The user has to be loggedIn in order to create an organization. After successfully logging in, the access is token returned back. The access token would then be used to update the organization name ,lunch price and currency on the table.
- **Parameters**: None
- **Example usage**:

  _Request Headers:_
  `Authorization: Bearer <access_token>`

  _Request Body:_
  `Content-Type: application/json`

  _Example PUT request_

  ```
  PUT /api/organization/create`
  Content-Type: application/json
    {
          "name": "example organisation",
          "lunch_price": "" // default to "#1000" if not set
          "currency":"currency detail"
    }
  ```

- **Example response(success)**:

  _organization created successfully_

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

- **Example Error responses:**:

  _authentication failure_

  - Content-Type: application/json

  ```
  HTTP/1.1  401 Unauthorized

    {
    "error": Authentication failed.",
    }
  ```

  _Forbidden_

  - Content-Type: application/json

  ```
  HTTP/1.1  403 Forbidden

    {
    "error": User not authorized to create an organization.",
    }
  ```

  _Bad request or invalid data:_

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

- **Endpoint**: `/api/organization/invite`
- **Method**: `POST`
- **Description**: This endpoint allows an admin user to send an invitation to users to join an organization
- **Parameters**: None
- **Example usage**:

  _Request Headers:_
  `Authorization: Bearer <access_token>`

  _Request Body:_
  `Content-Type: application/json`

  _Example POST request_

  ```
  POST /api/organization/invite
  Content-Type: application/json

  {
      "email": "kurves@orglunch.com"
  }
  ```

- **Example response(success)**:

  _organization invite created successfully_

  status: status.HTTP*201_CREATED
  \_Response Body*

  ```
  {
  "message": "success",
  "statusCode": 200,
  "data": null
  }
  ```

- **Example Error responses**:

  _Bad request or invalid data_

  - Content-Type: application/json

  ```
  HTTP/1.1  400 Bad Request
  Content-Type: application/json
    {
    "error": "Field 'email' must be a string.",
    }
  ```

  _authentication failure_

  - Content-Type: application/json

  ```
  HTTP/1.1  401 Unauthorized

    {
    "error": Authentication failed.",
    }
  ```

  _Forbidden_

  - Content-Type: application/json

  ```
  HTTP/1.1  403 Forbidden

    {
    "error": User not authorized to create an organization invite.",
    }
  ```

### Create Organization Wallet

- **Endpoint**: `/create/`
- **HTTP Method**: POST
- **Description**: Create an organization's wallet.
- **Parameters**:
  - `data` (in body, required) - Organization wallet data. See [OrganizationLunchWallet](#organizationlunchwallet) for details.
- **Responses**:
  - `201` - Organization wallet created successfully.
  - `400` - Bad Request
- **Tags**: create

### Get Organization Balance

- **Endpoint**: `/get_balance/{organization_id}/`
- **HTTP Method**: GET
- **Description**: Get the balance of an organization's wallet.
- **Parameters**:
  - `organization_id` (in path, required) - The unique identifier of the organization.
- **Responses**:
  - `200` - Balance retrieved successfully.
- **Tags**: get_balance

### List All Lunches

- **Endpoint**: `/lunch/all`
- **HTTP Method**: GET
- **Description**: List all lunches.
- **Responses**:
  - `200` - Successfully fetched lunches. Response schema: array of [Lunch](#lunch)
- **Tags**: lunch

### Send a Lunch

- **Endpoint**: `/lunch/send`
- **HTTP Method**: POST
- **Description**: Send a lunch to another user.
- **Responses**:
  - `201` - Lunch request created successfully.
- **Tags**: lunch

### Delete a Lunch

- **Endpoint**: `/lunch/{id}`
- **HTTP Method**: DELETE
- **Description**: Delete a lunch transaction.
- **Parameters**:
  - `id` (in path, required) - The unique identifier of the lunch transaction.
- **Responses**:
  - `204` - Lunch transaction deleted successfully.
- **Tags**: lunch

### Search for a User

- **Endpoint**: `/search/{name_or_email}/`
- **HTTP Method**: GET
- **Description**: API view accepting either a name (first or last) or email parameter to search for a user.
- **Parameters**:
  - `name_or_email` (in path, required) - Name or email to search for.
- **Responses**:
  - `200` - User found.
- **Tags**: search

### List All Users

- **Endpoint**: `/users/`
- **HTTP Method**: GET
- **Description**: List all users and get their details.
- **Responses**:
  - `200` - List of users. Response schema: array of [UserList](#userlist)
- **Tags**: users

### User Login

- **Endpoint**: `/users/login/`
- **HTTP Method**: POST
- **Description**: Log in a user.
- **Responses**:
  - `201` - User logged in successfully.
- **Tags**: users

### Get User Details

- **Endpoint**: `/users/{id}/`
- **HTTP Method**: GET
- **Description**: Get a user's details.
- **Parameters**:
  - `id` (in path, required) - The unique identifier of the user.
- **Responses**:
  - `200` - User details. Response schema: [UserList](#userlist)
  - `404` - User does not exist.
  - `403` - Permission denied.
- **Tags**: users

### Delete User

- **Endpoint**: `/users/{id}/`
- **HTTP Method**: DELETE
- **Description**: Delete a user.
- **Parameters**:
  - `id` (in path, required) - The unique identifier of the user.
- **Responses**:
  - `204` - User deleted.
  - `404` - User does not exist.
  - `403` - Permission denied.
- **Tags**: users

### Get User's Lunch

- **Endpoint**: `/users/{user_id}/lunches/{lunch_id}`
- **HTTP Method**: GET
- **Description**: Get a user's lunch transaction.
- **Parameters**:
  - `user_id` (in path, required) - The unique identifier of the user.
  - `lunch_id` (in path, required) - The unique identifier of the lunch transaction.
- **Responses**:
  - `200` - Lunch details. Response schema: [Lunch](#lunch)
  - `404` - Detail not found.
  - `403` - Permission denied.
- **Tags**: users

### Get User's Organization

- **Endpoint**: `/users/{user_id}/organizations/{org_id}`
- **HTTP Method**: GET
- **Description**: Get a user's organization details.
- **Parameters**:
  - `user_id` (in path, required) - The unique identifier of the user.
  - `org_id` (in path, required) - The unique identifier of the organization.
- **Responses**:
  - `200` - Organization details. Response schema: [Organization](#organization)
  - `404` - Organization not found for this user.
  - `403` - Permission denied.
- **Tags**: users

### Request a Withdrawal

- **Endpoint**: `/withdrawal/request`
- **HTTP Method**: POST
- **Description**: Request a withdrawal.
- **Parameters**:
  - `data` (in body, required) - Withdrawal request data. See [WithdrawalRequest](#withdrawalrequest) for details.
- **Responses**:
  - `201` - Withdrawal request created successfully.
  - `400` - Bad Request
- **Tags**: withdrawal

### Get Withdrawal Details

- **Endpoint**: `/withdrawals/{id}/`
- **HTTP Method**: GET
- **Description**: Get withdrawal details.
- **Parameters**:
  - `id` (in path, required) - The unique identifier of the withdrawal.
- **Responses**:
  - `200` - Withdrawal details. Response schema: [Withdrawal](#withdrawal)
- **Tags**: withdrawals

### Update Withdrawal

- **Endpoint**: `/withdrawals/{id}/`
- **HTTP Method**: PUT
- **Description**: Update withdrawal details.
- **Parameters**:
  - `id` (in path, required) - The unique identifier of the withdrawal.
  - `data` (in body, required) - Withdrawal data. See [Withdrawal](#withdrawal) for details.
- **Responses**:
  - `200` - Withdrawal updated successfully. Response schema: [Withdrawal](#withdrawal)
- **Tags**: withdrawals

## Definitions

### UserRegistration

User registration data.

#### Properties

- `email` (string, required, format: email, max length: 225, min length: 1) - Email address.
- `password` (string, required, max length: 128, min length: 1) - Password.
- `first_name` (string, required, max length: 225, min length: 1) - First name.
- `last_name` (string, max length: 225) - Last name (optional).
- `phone` (string, max length: 20) - Phone number (optional).

### OrganizationLunchWallet

Organization wallet data.

#### Properties

- `balance` (string, required, format: decimal) - Balance.
- `org_id` (integer, required) - Organization ID.

### Lunch

Lunch transaction data.

#### Properties

- `id` (integer, read-only) - ID.
- `receiver_id` (string, read-only) - Receiver ID.
- `sender_id` (integer) - Sender ID.
- `quantity` (integer, max: 4294967295, min: 0) - Quantity.
- `redeemed` (boolean) - Redeemed.

### ListInvites

Invitation data.

#### Properties

- `id` (integer, read-only) - ID.
- `email` (string, required, format: email, max length: 254, min length: 1) - Email address.
- `token` (string, max length: 20, min length: 1) - Token.
- `TTL` (string, format: date-time, read-only) - TTL.
- `org_id` (integer) - Organization ID.

### Organization

Organization data.

#### Properties

- `name` (string, required, max length: 255, min length: 1) - Name.
- `lunch_price` (string, format: decimal) - Lunch price.
- `currency` (string, max length: 3, min length: 1) - Currency.

### UserList

User details.

#### Properties

- `id` (integer, read-only) - ID.
- `org_id` (integer, optional) - Organization name.
- `first_name` (string, required, max length: 225, min length: 1) - First name.
- `last_name` (string, optional, max length: 225) - Last name.
- `profile_pic` (string) - Profile picture.
- `email` (string, required, format: email, max length: 225, min length: 1) - Email address.
- `phone` (string, optional, max length: 20) - Phone number.
- `created_at` (string, format: date-time, read-only) - Created date.
- `updated_at` (string, format: date-time, read-only) - Updated date.
- `lunch_credit_balance` (string, max length: 50, min length: 1) - Lunch credit.

### WithdrawalRequest

Withdrawal request data.

#### Properties

- `bank_name` (string, required, max length: 100, min length: 1) - Bank name.
- `bank_number` (string, required, max length: 20, min length: 1) - Bank number.
- `bank_code` (string, required, max length: 20, min length: 1) - Bank code.
- `amount` (string, format: decimal, required) - Amount.

### Withdrawal

Withdrawal data.

#### Properties

- `id` (integer, read-only) - ID.
- `status` (string, enum: ["redeemed", "not_redeemed"]) - Withdrawal status.
- `amount` (string, format: decimal, required) - Withdrawal amount.
- `created_at` (string, format: date-time, read-only) - Withdrawal timestamp.
- `updated_at` (string, format: date-time, read-only) - Updated timestamp.
- `user_id` (integer) - User ID.
