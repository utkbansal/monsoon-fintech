MonsoonFintech Interview
========================


Setup Instructions
------------------

* Install Java - `brew cask install java`
* Install Python dependencies - `pip install -r requirements.txt`
* Add database username and password in `settigns.py`
* Create blank mysql db named `monsoon`
* Run migrations `python manage.py migrate`
* Finally run the server `python manage.py runserver`