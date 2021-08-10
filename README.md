# About shipengine-python
This library is designed to make accessing the ShipEngine.com API easy and standard.

# Installation (API-KEY)
The ShipEngine.com API requires an API-Key be sent with each request.  The API-Key should
be specified by setting an environment variable called SHIP_ENGINE_API_KEY.

# Dependencies
* Python >= 3.1
* requests==2.11.1
* vcrpy==1.10.3
* pytest==3.0.3

# TODO
* Write tests for modules
    * accounts
    * batches
    * insurance
    * manifests
    * packages
    * rates
    * tracking
    * warehouses
    * webhooks
* Implement Classes for modules
    * accounts
    * batches
    * insurance
    * manifests
    * packages
    * rates
    * tracking
    * warehouses
    * webhooks

# License
This library is distributed under GNU LGPL version 2.1, which can be found in the file "doc/LGPL". I reserve the right to place future versions of this library under a different license. https://www.gnu.org/copyleft/lesser.html

This basically means you can use shipengine-python in any project you want, but if you make any changes or additions to shipengine-python itself, those must be released with a compatible license (preferably submitted back to the shipengine-python project). Closed source and commercial applications are fine.
