Project 9: Improve a Django Project
===================================

**WARNING: Security Vulnerability**  
There are multiple vulnerabilities with versions of Django below 1.11.19 (see [CVE-2019-6975](https://nvd.nist.gov/vuln/detail/CVE-2019-6975), [CVE-2019-3498](https://nvd.nist.gov/vuln/detail/CVE-2019-3498), [CVE-2017-7234](https://nvd.nist.gov/vuln/detail/CVE-2017-7234), and [CVE-2017-7233](https://nvd.nist.gov/vuln/detail/CVE-2017-7233)). These vulnerabilities have not been addressed as part of the project specification is to use the packages according to the supplied `requirements.txt`<sup>[1](#footnote1)</sup>.


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

- [x] <sup>[1](#footnote1)</sup> Use the provided `requirements.txt` to install needed packages for the project
- [x] Use `django-debug-toolbar` to find places where the database queries:
  - [x] run too long (max 60ms)
  - [x] hit the database too many times (max 5 queries)
- [x] Use `django-debug-toolbar` to find places where the templates aren't properly using inheritance
- [x] Appropriate Model Fields
  - [x] Check that the models are using appropriate fields for the type of data they store. 
  - [x] If not, correct them and
  - [x] create migrations to handle the data
- [x] Forms
  - [x] Check forms are using correct fields and validation
  - [x] If not, fix
- [x] Tests
  - [x] Use `coverage.py` to check code coverage (min 75%)
- [ ] Complies with most common PEP 8 standards of style.

### Extra Credit Features ###

- [x] Increase test coverage to >= 90%
- [x] Decrease combined query times on all views to 60ms or less
- [x] Add migrations to correct existing data when data types change
- [x] Add custom form validators

Testing
-------

TODO



Footnotes
---------
1. <a name="footnote1"> </a> Note that one deviation has been made from the Treehouse-provided `requirements.txt`: the version of django-debug-toolbar specified by `requirements.txt` is exactly v1.0 and the version of Django specified in the same file is exactly v1.9.9. However, django-debug-toolbar 1.0 is explicitly incompatible with Django 1.9.9. To make the project application run it was necessary to substitute a newer version of django-debug-toolbar, in this case v1.9.1. The version of `requirements.txt` in this repo was [adjusted accordingly](https://github.com/Crossroadsman/treehouse-techdegree-python-project9/compare/4c395e2..d671e92#diff-bba1be146e707ced497270bb4a686fa0).
