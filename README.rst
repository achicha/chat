Async Client-Server chat written in python.
=================


Quick start
-------
.. code::

   pip install aiogbchat --upgrade  # install
   python -m aiogbserver  -- nogui  # run server in console mode
   python -m aiogbclient            # run client in GUI mode

Documentation:
-------
`<https://achicha.github.io/chat/>`_


Known issues:
-------

* client disconnected with some logged issues (DB/asyncio). its not critical :)
* windows: client doesn't work in console mode.
* windows8 and higher: only works with pyqt5==5.9.2
* tests

Helpful:
-------

* How to generate docs:

.. code::

   pip install sphinx
   sphinx-apidoc -f ../../chat -o /some_dir/docs/source
   make html

* How to deploy to pypi:

.. code::

   pip install twine
   python3 setup.py bdist_wheel # generate wheel
   twine upload dist/*

Links:
-------

* `Add sphinx pages to github <https://daler.github.io/sphinxdoc-test/includeme.html>`_
