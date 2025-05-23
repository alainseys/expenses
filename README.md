# Expenses
This application create a sql lite database and keeps track of users expenses.

Users can create a account and enter the expenses

## Installation
- Create a .env file 
- Create a site key (SITE_KEY: unique key)
- Create a location for the database (APP_DB)

The application is best used with docker and visual studio code there is a devcontainer in this project. So when you clone this repo you get a prompt in VScode to build the container.

This wil install all of the python depenencies that are in a requirements file.

## Look and feel
You can change the look and feel by updating the templates in the templates folder i have used bootstrap but feel free to use something else like example tailwind.


## Models
Ther are a few basic models you can edit 
- Entry (manage the entry of new records)
- User (manages the users of the application)

## Routes
The routes you can find in the main logic of the application app.py

## To implement Features
- When end of the month export results to a table
- Exportable results to csv or PDF
- Shared accounts 