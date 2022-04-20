.. Qord documentation master file, created by
   sphinx-quickstart on Sun Feb  6 15:07:27 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Qord's documentation!
================================

Python library for Discord API based around asyncio.

**Features:**

- Object oriented, user friendly interface with no dirty payloads.
- Easy to customise and manage.
- Robust handling of HTTP ratelimits.
- Supports automatic gateway sharding.

.. note::
   Qord is currently under it's initial development (alpha) stage. During this phase, There may
   be breaking changes and public user-facing API should not be considered stable. There would
   be no efforts in keeping backward compatibility. While the library currently supports the
   basic functionalities required to build a bot, many essential features are yet to be
   implemented and for this reason, Qord isn't yet a library to choose for making full fledged
   bots.

   The complete lifetime of 0.x version is considered the development phase. More info about
   this `semantic versioning specification is found here. <https://semver.org/#spec-item-4>`_

.. toctree::
   :maxdepth: 1
   :caption: Table of Content:

   api/index
   getting_started
   releases

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
