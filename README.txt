Introduction
============

Provides basic listing components which display articles contained in the article.

The following features for raptus.article are provided by this package:

Components
----------
    * Listing columns (List of the contained articles arranged in columns.)
    * Listing left (List of the contained articles with their image on the left side.)
    * Listing right (List of the contained articles with their image on the right side.)

Dependencies
------------
    * raptus.article.nesting

Installation
============

To install raptus.article.listings into your Plone instance, locate the file
buildout.cfg in the root of your Plone instance directory on the file system,
and open it in a text editor.

Add the actual raptus.article.listings add-on to the "eggs" section of
buildout.cfg. Look for the section that looks like this::

    eggs =
        Plone

This section might have additional lines if you have other add-ons already
installed. Just add the raptus.article.listings on a separate line, like this::

    eggs =
        Plone
        raptus.article.listings

Note that you have to run buildout like this::

    $ bin/buildout

Then go to the "Add-ons" control panel in Plone as an administrator, and
install or reinstall the "raptus.article.default" product.

Note that if you do not use the raptus.article.default package you have to
include the zcml of raptus.article.listings either by adding it
to the zcml list in your buildout or by including it in another package's
configure.zcml.

Usage
=====

Components
----------
Navigate to the "Components" tab of your article and select one of the listing
components and press "save and view". Note that at least one article has to be contained
in the article in which this component is active.

Copyright and credits
=====================

raptus.article is copyrighted by `Raptus AG <http://raptus.com>`_ and licensed under the GPL. 
See LICENSE.txt for details.
