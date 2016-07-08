.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

====================
Date Search Extended
====================

This module adds date fields to make date search functions more complete.

Installation
============

Normal installation.

Usage
=====

Inherit this module and add a python file with the following code:

Sample on account move lines

    from openerp import models

    class AccountMoveLine(models.Model):
        _name = 'account.move.line'
        _inherit = ['account.move.line', 'date.search.mixin']

        _SEARCH_DATE_FIELD = 'date'


This will add search feature by year / month and day for 

Credits
=======

Contributors
------------

* Sylvain LE GAL <https://twitter.com/legalsylvain>
