# expense-tracker
Expense tracker is a personal finance tool that is designed to organize and track a range of expenses.
Your ongoing expenses are recorded by date and are easily being tracking by the application:

* The application allows flexibility by maintaining personal preferences such as expense categories and payment methods. 
* The application provides insights into your spending habits, using the filters.
* You can modify or delete the records that you have created.

### Application link
http://milanab.pythonanywhere.com/

#### Run the Expense application on your local computer:

### Prerequisites
1. Download the App to a local directory
2. Set up a Python development environment, including Python, pip, and virtualenv:  
`virtualenv env source env/bin/activate pip install -r requirements.txt`
3. Run the Django migrations to set up your models:   
```
python manage.py makemigrations 
python manage.py makemigrations expense_app 
python manage.py migrate
```
4. Start a local web server:  
`python manage.py runserver`
5. In your browser, go to http://localhost:8000

### High level flow
1. Register to the application
2. Define your personal preferences on the "Preferences" tab
3. Add your expenses on the "New Expense" tab
