### Update user details and user profile picture

## Description
<!--- I added two endpoints to patch details of user and user profile picture-->

## Motivation and Context
Why is this change required? These endpoints allow the user Update their details and profile picture 

## How Has This Been Tested?
<!--- Please describe in detail how you tested your changes. -->
I have tested the endpoints using Postman
<!--- Include details of your testing environment, and the tests you ran to -->
{
    "status": "success",
    "message": "User updated successfully",
    "data": {
        "first_name": "Abdul-Malik",
        "last_name": "Adebayo",
        "phone": null,
        "bank_number": null,
        "bank_code": null,
        "bank_name": null,
        "lunch_credit_balance": "5000"
    }
}

## Screenshots (if appropriate):
![Screenshot (197)](https://github.com/hngx-org/Mirage-food-backend/assets/65060993/9574b5d8-5894-4b11-993f-c01b408eaf92)

## Types of changes
- [x] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)

## Checklist:
- [x] My code follows the code style of this project.
- [x] My change requires a change to the documentation.
- [x] I have updated the documentation accordingly.
- [ ] I have read the **CONTRIBUTING** document.
- [x] I have added tests to cover my changes.
- [x] All new and existing tests passed.
