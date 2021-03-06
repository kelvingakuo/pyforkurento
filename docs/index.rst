Welcome to pyforkurento's documentation!
========================================

`pyforkurento <https://pypi.org/project/pyforkurento/>`_ is a Python client for `Kurento Media Server <https://doc-kurento.readthedocs.io>`_ (KMS). This SDK was built because (currently) only Node, Angular and Bower clients exist.

The documentation for this SDK project is organized into different sections:

- :ref:`setup`
- :ref:`recipes`
- :ref:`api`

.. _setup:

.. toctree::
   :maxdepth: 2
   :caption: Setup

Setup
==================
1. Install Kurento Media Server

::

   sudo docker run --name kms -d -p 8888:8888 kurento/kurento-media-server

2. Install pyforkurento

::

   pip install pyforkurento

3. pyforkurento runs as an application server. You'll need to install relevant packages for the web or mobile client

For Node, Angular etc.

::

   npm install kurento-utils

For vanilla Javascript, the steps are:

I. Install Node and NPM

II. Install Bower

III. Unpack Kurento-Utils using Bower. In any dir:

::

   bower install kurento-utils

Inside ```bower_components/kurento_utils/js``` find the file ```kurento-utils.min.js```. Copy it to your working area


Optional Setup
==================
1. To use GStreamer filters

::

   sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio


2. To develop custom filters

::

   sudo apt-get update && sudo apt-get install --yes kurento-media-server-dev

If you get the error: *Unable to locate package kurento-media-server-dev* try the following:

1. Open `this link <https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/Kurento/kurento-media-server/tree/master/scaffold>`_ in your browser
2. Extract the downloaded folder to a location of choice
3. ```cd``` into that folder then test using:

::

   sh kurento-module-scaffold.sh TestKMSFilter ../custom_kurento_module opencv_filter



.. _recipes:
 
.. toctree::
   :maxdepth: 2
   :caption: Recipes

Recipes
==================
**Before** you start using ```pyforkurento```, make sure you have a pretty good understanding of KMS. Go through `this refresher <https://doc-kurento.readthedocs.io/en/stable/features/kurento_api.html>`_ first.

Follow the instructions in the `recipes dir here <https://github.com/kelvingakuo/pyforkurento/tree/master/recipes>`_.

.. _api:

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   client
   media_pipeline
   media_element
   endpoints
   filters
   hubs
