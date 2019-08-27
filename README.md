Project 9: Improve a Django Project
===================================

Installation
------------
- Clone the rep
- Create and activate a venv
- To run the application install the required packages using `pip install -r requirements.txt` from the 
  [`improve_django_v3`](https://github.com/Crossroadsman/treehouse-techdegree-python-project9/tree/master/improve_django_v3) folder
- To run tests and generate coverage reports also install the test-specific packages using `pip install -r test_requirements.txt`

Usage
-----
- The application can be run using `python manage.py runserver 0:8000`
- Tests can be run using `python manage.py test`. Detailed HTML test reports will be generated and saved in the cover subdirectory

Feature Checklist
-----------------

### Base Features ###

- [ ] Use the provided `requirements.txt` to install needed packages for the project
- [ ] Use `django-debug-toolbar` to find places where the database queries:
  - [ ] run too long
  - [ ] hit the database too many times
- [ ] Use `django-debug-toolbar` to find places where the templates aren't properly using inheritance
- [ ] Appropriate Model Fields
  - [ ] Check that the models are using appropriate fields for the type of data they store. 
  - [ ] If not, correct them and
  - [ ] create migrations to handle the data
- [ ] Forms
  - [ ] Check forms are using correct fields and validation
  - [ ] If not, fix
- [ ] Tests
  - [ ] Use `coverage.py` to check code coverage (min 75%)
- [ ] Complies with most common PEP 8 standards of style.

### Extra Credit Features ###

- [ ] Increase test coverage to >= 90%
- [ ] Decrease combined query times on all views to 60ms or less
- [ ] Add migrations to correct existing data when data types change
- [ ] Add custom form validators

Testing
-------

TODO
