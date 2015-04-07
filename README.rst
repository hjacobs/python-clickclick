===========
Click Click
===========

.. image:: https://travis-ci.org/zalando/python-clickclick.svg?branch=master
   :target: https://travis-ci.org/zalando/python-clickclick
   :alt: Travis CI build status

.. image:: https://coveralls.io/repos/zalando/python-clickclick/badge.svg
   :target: https://coveralls.io/r/zalando/python-clickclick

Utility functions for the wonderful `Click library`_.
Click is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.


Usage
=====

.. code-block:: python

    from clickclick import Action

    with Action('Performing remote call..') as act:
        do_something()
        act.progress()
        do_something_else()


.. _Click library: http://click.pocoo.org/3/

License
=======

Copyright © 2015 Zalando SE

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
