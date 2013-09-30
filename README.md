databin
=======

databin is a simple tool that allows you to share tables via the web just like other paste bins would let you share code and text.

The code is based on SQLAlchemy, Flask and sniffing glue. If you want to install it, make sure you have ``foreman`` installed (e.g.
via brew or apt), then create a ``virtualenv`` before you:

    pip install -r requirements.txt
    python setup.py develop 
    foreman start 

And remember: tables are for friends.

