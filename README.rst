===========
 automgtic
===========

automgtic is an automatic media uploader for GNU MediaGoblin.

----------
 Features
----------

automgtic authenticates to the GNU MediaGoblin server via `OAuth draft v2.25`_.

automgtic uses a local database to keep track of the files where it stores:

- An MD5 digest of the file to prevent multiple uploads of the same file due to
  filesystem changes.
- The filename of the file when it was uploaded.
- The metadata returned by the GNU MediaGoblin server when the file was posted.

.. _`oauth draft v2.25`: http://tools.ietf.org/html/draft-ietf-oauth-v2-25

--------------
 Installation
--------------

To install automgtic, download the files or clone the repo, then ``cd`` to the
directory containing the ``automgtic.ini`` file and run::

    virtualenv .  # Create a new python virtualenv
    . bin/activate  # Activate the virtualenv
    python setup.py develop  # Fetch all the dependencies into your virtualenv
    # !! - This is a single command split up on two lines
    python -c "from automgtic.models import Base, engine
    Base.metadata.create_all(engine)" # Create the DB tables


-------
 Usage 
-------

Once you have installed the dependencies, you need to have an OAuth client
registered on the GNU MediaGoblin instance, you can register one at
``instance.example/oauth/client/register``.

Once you have registered your OAuth client you need the client identifier in
your config.

.. warning::
    Before you start editing your config, do ``cp automgtic.ini
    automgtic_local.ini``, this to separate the version-controlled
    ``automgtic.ini`` from your local settings.

When the ``client_id`` is set, run ``./run.py --authorize``, then follow the
instructions provided. This will update your ``.ini`` with the ``access_token``
field and you will be ready to upload media with automgtic.

To upload media from a directory, simply run ``./run.py --run <directory>``.
