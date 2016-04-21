.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Ionic Apps - Badge Reader
=========================

Provide light JS apps that provides badge reader interface.

Authentication
--------------

User must select Database name, login and password. (The user must be
member of the new group 'Badge Reader')

.. image:: /badge_reader/static/description/login.png

User Search
-----------

User should scan User barcode.

.. image:: /badge_reader/static/description/user_search.png

If the barcode is unknown a specific sound is played.

.. image:: /badge_reader/static/description/user_search_fail.png

Partner Form
------------

If the barcode matches with a user, the partner is display with some
information, depending on his status.

.. image:: /louve_custom_pos/static/description/partner_form.png

Technical Information
---------------------

* Create a new group 'Badge Reader' (badge_reader.user). User must be member
  of that group to log into the apps;

TODO
====

* retirer les fichiers inutiles de lib;
* rendre fonctionnel l'affichage des images partenaire;
* retirer TODO;
* ajouter FR translation + screenshot;

Possible Improvments
====================

* display partner with bootstrap colors in kanban and tree view

Credits
=======

Contributors
------------

* Sylvain LE GAL <https://twitter.com/legalsylvain>

Icon module comes from <https://www.iconfinder.com/icons/52644/card_reader_security_icon> and is copyright by <www.tpdkdesign.net>

