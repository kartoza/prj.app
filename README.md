projecta
================

[![Join the chat at https://gitter.im/kartoza/projecta](https://badges.gitter.im/kartoza/projecta.svg)](https://gitter.im/kartoza/projecta?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Build Status](https://travis-ci.org/kartoza/projecta.svg?branch=develop)](https://travis-ci.org/kartoza/projecta)
[![Stories in Ready](https://badge.waffle.io/kartoza/projecta.png?label=ready)](http://waffle.io/kartoza/projecta)
[![Stories in In Progress](https://badge.waffle.io/kartoza/projecta.png?label=in progress)](http://waffle.io/kartoza/projecta)


A django app for creating visual changelogs for software releases, and for managing a software project at a high level.

View a running instance at [http://changelog.kartoza.com](http://changelog.kartoza.com)

intercom.io
-----------
If you wish to make use of [intercom.io](https://www.intercom.io), include a
`private.py` file in `core.settings` with your `INTERCOM_APP_ID` as a string.
The necessary code snippet is already included in `project_base.html`.

rst output
----------
To be able to download data as rst files, you need to install pandoc

    sudo apt-get install pandoc  # on debian
