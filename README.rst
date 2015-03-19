===========
Click Click
===========

Utility functions for the wonderful `Click library`_.
Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.


Usage
=====

.. code-block:: python

    from click.click import Action

    with Action('Performing remote call..') as act:
        do_something()
        act.progress()
        do_something_else()


.. _Click library: http://click.pocoo.org/3/
