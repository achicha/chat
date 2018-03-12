Async Client-Server chat written in python.
=================


Quick start
-------
.. code::

   pip install aiogbchat --upgrade  # install
   python -m aiogbserver.main     # run server
   python -m aiogbclient.main     # run client

Documentation:
-------
`<https://achicha.github.io/chat/>`_


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
