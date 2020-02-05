A python client for Kurento Media Streamer

## CONTENTS
1. [Changelog](#change)

## USAGE
1. Install Kurento
```bash
sudo docker run --name kms -d -p 8888:8888 kurento/kurento-media-server
```

**DO NOT USE THIS SDK IN ANY FORM OF A PRODUCTION ENVIRONMENT**

The implementation of this SDK was inspired by [this abandoned project](https://github.com/minervaproject/pykurento/tree/master/pykurento)

### REFERENCE DOCUMENTATION
https://github.com/Kurento/doc-fiware-readthedocs/blob/master/apib/stream_oriented_open_api.apib


## CHANGELOG <a id = "change"></a>
*This changelog follows a loose version of semantic versioning*
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
