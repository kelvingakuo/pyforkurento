A python client for Kurento Media Streamer

## CONTENTS
1. [Changelog](#change)

## USAGE
1. Install Kurento
```bash
sudo docker run --name kms -d -p 8888:8888 kurento/kurento-media-server
```

2. Install PyForKurento
```bash
pip install pyforkurento
```

[Optional] To develop custom filters;
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

**DO NOT USE THIS SDK IN ANY FORM OF A PRODUCTION ENVIRONMENT**

The implementation of this SDK was inspired by [this abandoned project](https://github.com/minervaproject/pykurento/tree/master/pykurento)

### REFERENCE DOCUMENTATION



## CHANGELOG <a id = "change"></a>
*This changelog follows a loose version of semantic versioning*
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
