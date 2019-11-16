Fyyur
-----

### Introduction

This is the repo for project #1 of the Udacity Fullstack Developer nanodegree.

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.


### Tech Stack

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend


Overall:
* Models are located in `models.py`.
* Controllers are located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`.
* `templates/layouts` -- Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- Defines the forms used to create new artists, shows, and venues.
* `app.py` --  Defines routes that match the user’s URL, and controllers which handle data and renders views to the user.
* `models.py` -- Defines the data models that set up the database tables.
* `config.py` -- Stores configuration variables and instructions.


### Development Setup and Demo

To demo the Fyyur app,

1. Clone the repo:
  ```
  $ git clone https://github.com/benschaaff/Fyyur.git
  ```

2. Environment setup -- this will install the dependencies and setup flask to run in development mode:
  ```
  $ cd Fyyur/
  $ bash setup.sh
  ```

3. Start the server:
  ```
  $ bash run.sh
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)
