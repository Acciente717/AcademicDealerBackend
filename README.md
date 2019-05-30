# AcademicDealerBackend

## Dependencies

+ django
+ mysql

## How to Run

+ Add a superuser called `root` with password `password` in mysql
+ Create a database called `academic_dealer` in `mysql`
+ Run following scripts to start
    + `python3 manage.py makemigrations`
    + `python3 manage.py migrate`
    + `python3 manage.py runserver`

## For Debug
+ Create a superuser by `python3 manage.py createsuperuser`
+ Visit `http://url:port/admin/` and login
+ Manually edit database