.. currentmodule:: qord

Errors and Exceptions
=====================

These are the special exceptions raised by the library in certain scenarios. All of these
exceptions inherit a common :exc:`QordException` class.

QordException
~~~~~~~~~~~~~

.. autoexception:: QordException()

ClientSetupRequired
~~~~~~~~~~~~~~~~~~~

.. autoexception:: ClientSetupRequired()

HTTPException
~~~~~~~~~~~~~

.. autoexception:: HTTPException()

HTTPBadRequest
~~~~~~~~~~~~~~

.. autoexception:: HTTPBadRequest()

HTTPForbidden
~~~~~~~~~~~~~

.. autoexception:: HTTPForbidden()

HTTPNotFound
~~~~~~~~~~~~

.. autoexception:: HTTPNotFound()

HTTPServerError
~~~~~~~~~~~~~~~

.. autoexception:: HTTPServerError()

ShardException
~~~~~~~~~~~~~~

.. autoexception:: ShardException()

ShardCloseException
~~~~~~~~~~~~~~~~~~~

.. autoexception:: ShardCloseException()

MissingPrivilegedIntents
~~~~~~~~~~~~~~~~~~~~~~~~

.. autoexception:: MissingPrivilegedIntents()
