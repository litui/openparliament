A site that scrapes and republishes information on Canada's House of Commons.

This branch is for a work-in-progress selective export-to-wordpress
capability for use with Custom Post Type UI and Advanced Custom Fields.

License
=======

Code is released under the AGPLv3 (see below). However, any site you create
using this code cannot use the openparliament.ca name or logo, except as
acknowledgement.

Copyright (C) 2012 Michael Mulley (michaelmulley.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

Installation
============

This guide briefly covers a local development install. These instructions
aren't suitable for a live, online instance.

You need Python 2.6 or 2.7. If you want search to work, you'll need Solr 3.5+.

Environment setup
--------------------

You should have virtualenv and pip installed. Create a new virtualenv, and install dependencies:

    pip install -r requirements.txt
    
Database
-----------

The site's pretty useless without some data. Download a dump of the openparliament data
from <http://openparliament.ca/data-download/>

Save the SQLite database as `parliament.sqlite`, in the main project directory (same one `manage.py` is in).

Settings
-----------

Copy `settings.py.example` to `settings.py`. Customize it as necessary (though it should work out of the box).

Run `python manage.py migrate` to ensure the database schema is up-to-date.

Start the development server
-------------------------------

    python manage.py runserver
    
If things went well, you should now be able to access your own instance of openparliament at `http://127.0.0.1:8000/`.

The site is built around scrapers, and various jobs are available to scrape data. See `jobs.py` for a list of jobs; invoke them via, for example, `manage.py job twitter`. (Please be polite and don't scrape sites, especially parl.gc.ca sites, unnecessarily.)
