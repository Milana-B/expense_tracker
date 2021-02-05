# expense-tracker

Expense tracker app is personal finance tool that provides a platform for tracking a range of expenses.
The user enters outgoing money, and the app can help him store and track that information.
The system allows flexibility by maintaining personal preferences such as expense categories and payment methods.
The app provides insight into user’s spending habits by the filter feature

Link to App: http://milanab.pythonanywhere.com/


Run the Expense app on your local computer:

1. Download the App to a local directory

2. Set up a Python development environment, including Python, pip, and virtualenv:
    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
  
 3. Run the Django migrations to set up your models:
    python manage.py makemigrations
    python manage.py makemigrations polls
    python manage.py migrate
  
4. Start a local web server:
    python manage.py runserver
  
5. In your browser, go to http://localhost:8000
