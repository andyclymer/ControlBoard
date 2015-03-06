==========
 Appendix
==========

How To
======

Enable :rfc:`2217` in programs using pySerial.
    Patch the code where the :class:`serial.Serial` is instantiated. Replace
    it with::

        try:
            s = serial.serial_for_url(...)
        except AttributeError:
            s = serial.Serial(...)

    Assuming the application already stores port names as strings that's all
    that is required. The user just needs a way to change the port setting of
    your application to an ``rfc2217://`` :ref:`URL <URLs>` (e.g. by editing a
    configuration file, GUI dialog etc.).

    Please note that this enables all :ref:`URL <URLs>` types supported by
    pySerial and that those involving the network are unencrypted and not
    protected against eavesdropping.

Test your setup.
    Is the device not working as expected? Maybe it's time to check the
    connection before proceeding. :ref:`miniterm` from the :ref:`examples`
    can be used to open the serial port and do some basic tests.

    To test cables, connecting RX to TX (loop back) and typing some characters
    in :ref:`miniterm` is a simple test. When the characters are displayed
    on the screen, then at least RX and TX work (they still could be swapped
    though).


FAQ
===
Example works in :ref:`miniterm` but not in script.
    The RTS and DTR lines are switched when the port is opened. This may cause
    some processing or reset on the connected device. In such a cases an
    immediately following call to :meth:`write` may not be received by the
    device.

    A delay after opening the port, before the first :meth:`write`, is
    recommended in this situation. E.g. a ``time.sleep(1)``


Application works when .py file is run, but fails when packaged (py2exe etc.)
    py2exe and similar packaging programs scan the sources for import
    statements and create a list of modules that they package. pySerial may
    create two issues with that:

    - implementations for other modules are found. On Windows, it's safe to
      exclude 'serialposix', 'serialjava' and 'serialcli' as these are not
      used.

    - :func:`serial.serial_for_url` does a dynamic lookup of protocol handlers
      at runtime.  If this function is used, the desired handlers have to be
      included manually (e.g. 'serial.urlhandler.protocol_socket',
      'serial.urlhandler.protocol_rfc2217', etc.). This can be done either with
      the "includes" option in ``setup.py`` or by a dummy import in one of the
      packaged modules.

User supplied URL handlers
    :func:`serial.serial_for_url` can be used to access "virtual" serial ports
    identified by an :ref:`URL <URLs>` scheme. E.g. for the :rfc:`2217`:
    ``rfc2217:://``.

    Custom :ref:`URL <URLs>` handlers can be added by extending the module
    search path in :data:`serial.protocol_handler_packages`. This is possible
    starting from pySerial V2.6.


Related software
================

com0com - http://com0com.sourceforge.net/
    Provides virtual serial ports for Windows.


License
=======

Copyright (C) 2001-2013 Chris Liechti <cliechti(at)gmx.net>;
All Rights Reserved.

This is the Python license. In short, you can use this product in commercial
and non-commercial applications, modify it, redistribute it.  A notification to
the author when you use and/or modify it is welcome.


**TERMS AND CONDITIONS FOR ACCESSING OR OTHERWISE USING THIS SOFTWARE**

*LICENSE AGREEMENT*

1. This LICENSE AGREEMENT is between the copyright holder of this product, and
   the Individual or Organization ("Licensee") accessing and otherwise using
   this product in source or binary form and its associated documentation.

2. Subject to the terms and conditions of this License Agreement, the copyright
   holder hereby grants Licensee a nonexclusive, royalty-free, world-wide
   license to reproduce, analyze, test, perform and/or display publicly,
   prepare derivative works, distribute, and otherwise use this product alone
   or in any derivative version, provided, however, that copyright holders
   License Agreement and copyright holders notice of copyright are retained in
   this product alone or in any derivative version prepared by Licensee.

3. In the event Licensee prepares a derivative work that is based on or
   incorporates this product or any part thereof, and wants to make the
   derivative work available to others as provided herein, then Licensee hereby
   agrees to include in any such work a brief summary of the changes made to
   this product.

4. The copyright holder is making this product available to Licensee on an "AS
   IS" basis. THE COPYRIGHT HOLDER MAKES NO REPRESENTATIONS OR WARRANTIES,
   EXPRESS OR IMPLIED.  BY WAY OF EXAMPLE, BUT NOT LIMITATION, THE COPYRIGHT
   HOLDER MAKES NO AND DISCLAIMS ANY REPRESENTATION OR WARRANTY OF
   MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF
   THIS PRODUCT WILL NOT INFRINGE ANY THIRD PARTY RIGHTS.

5. THE COPYRIGHT HOLDER SHALL NOT BE LIABLE TO LICENSEE OR ANY OTHER USERS OF
   THIS PRODUCT FOR ANY INCIDENTAL, SPECIAL, OR CONSEQUENTIAL DAMAGES OR LOSS
   AS A RESULT OF MODIFYING, DISTRIBUTING, OR OTHERWISE USING THIS PRODUCT, OR
   ANY DERIVATIVE THEREOF, EVEN IF ADVISED OF THE POSSIBILITY THEREOF.

6. This License Agreement will automatically terminate upon a material breach
   of its terms and conditions.

7. Nothing in this License Agreement shall be deemed to create any relationship
   of agency, partnership, or joint venture between the copyright holder and
   Licensee. This License Agreement does not grant permission to use trademarks
   or trade names from the copyright holder in a trademark sense to endorse or
   promote products or services of Licensee, or any third party.

8. By copying, installing or otherwise using this product, Licensee agrees to
   be bound by the terms and conditions of this License Agreement.

