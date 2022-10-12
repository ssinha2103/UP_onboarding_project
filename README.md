# UP_onboarding_project

{% if False %}

# Introduction

The goal of this project is to provide minimalistic django project on:-

• A Web App 
• Database 
• RESTful API endpoints for: 
• Creating merchants, stores and items 
• APIs should handle list view, detail view, CRUD operations 
• Authentication! 
• Test-cases 

### Techs Used

- `Django`
- `MySQL`
- `JWT Authentication`
- `PyTest`
      
### Steps To Reciprocate


Installing inside virtualenv is recommended, however you can start your project without virtualenv too.



# Getting Started

    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    

Then simply make the migrations:

    $ python manage.py makemigrations
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver


### Endpoints for Now

- `//` It opens the home page for the web app where we can see all the listed endpoints.
- `/admin/` It opens the admin page for the Django app.
- `/register/` For registering users on the basis of Role that are Merchant and Consumer.
- `/login/` For logging in as Merchant or Consumer.
- `'token/obtain/'` For the reason, if the user wants to see his/her JWT token.
- `token/refresh` For the reason, if the user wants to update his/her JWT Token.
- `/stores/` Used by Merchant for adding a new and view their registered stores.
- `/items/` Used by Merchant for adding items under their Registered Stores.
- `/placeorders/` Used by consumer to place orders.
- `/seeorders/` Used used by the merchant to see the orders that have been placed that their registered stores.