projecta
================

[![Stories in Ready](https://badge.waffle.io/timlinux/projecta.png?label=ready)](http://waffle.io/timlinux/projecta)
[![Stories in In Progress](https://badge.waffle.io/timlinux/projecta.png?label=in progress)](http://waffle.io/timlinux/projecta)
[![Build Status](http://jenkins.linfiniti.com/buildStatus/icon?job=Projecta)](http://jenkins.linfiniti.com/job/Projecta/)


A django app for creating visual changelogs for software releases, and for managing a software project at a high level.

View a running instance at [http://changelog.linfiniti.com](http://changelog.linfiniti.com)

intercom.io
-----------
If you wish to make use of [intercom.io](https://www.intercom.io), include a
`private.py` file in `core.settings` with your `INTERCOM_APP_ID` as a string.
The necessary code snippet is already included in `project_base.html`.