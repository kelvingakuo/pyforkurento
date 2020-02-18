A python client for Kurento Media Streamer

## CONTENTS
1. [Setup](#setup)
2. [Sample Usage](#usage)
3. [Changelog](#change)

## SETUP <a id = "setup"></a>
1. Install Kurento
```bash
sudo docker run --name kms -d -p 8888:8888 kurento/kurento-media-server
```

2. Install pyforkurento
```bash
pip install pyforkurento
```

3. pyforkurento runs as an application server. You'll need to install relevant packages for the web or mobile client

For Node, Angular etc:
```bash
npm install kurento-utils
```

TODO: For vanilla Javascript:

[Optional] To use GStreamer filters:
```bash
sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

[Optional] To develop custom filters:
```bash
sudo apt-get update && sudo apt-get install --yes kurento-media-server-dev
```

If you get the error: *Unable to locate package kurento-media-server-dev* try:
1. Paste this link (https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/Kurento/kurento-media-server/tree/master/scaffold) to your browser
2. Extract the downloaded folder to a location of choice
3. ```cd``` into that folder then test using:
```bash
sh kurento-module-scaffold.sh TestKMSFilter ../custom_kurento_module opencv_filter
```

**This SDK is not yet 'prod-ready'** and was inspired by [this abandoned project](https://github.com/minervaproject/pykurento)


## SAMPLE USAGE <a id = "usage"></a>
**Before** you start using ```pyforkurento``` and have a pretty good understanding of KMS, go through [this refresher](https://doc-kurento.readthedocs.io/en/stable/features/kurento_api.html) first


**Read the complete documentation here: https://pyforkurento.readthedocs.io/en/latest/**



## CHANGELOG <a id = "change"></a>
*This changelog follows a loose version of semantic versioning*
### 0.1.6 18th Feb 2020
**Changed**
* ```create_endpoint()``` to ```add_endpoint()```

### 0.1.5 14th Feb 2020
**Improved**
* Documentation significantly, and hosted on readthedocs

### 0.1.4 13th Feb 2020
**Improved**
* Addition of event listeners to media elements

### 0.1.3 12th Feb 2020
**Improved**
* Creation of media elements in a media pipeline

**Fixed**
* Class inheritance structure

**Added**
* ImageOverlayFilter

### 0.0.2 5th Feb 2020
**Fixed**
* Class method parameters error

### 0.0.2 5th Feb 2020
**Fixed**
* Import error

### 0.0.1 5th Feb 2020
* Released a very basic version of the project under the name 'pyforkurento' with only the capability to:
    - Create:
        - Media Pipelines
        - Player Endpoints
        - WebRTC Endpoints
    - Subscribe to ICE candidates events on a WebRTC Endpoint
