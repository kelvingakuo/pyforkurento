A python client for Kurento Media Streamer

**This SDK is not yet 'prod-ready'** and was inspired by [this abandoned project](https://github.com/minervaproject/pykurento)

**This project is also now abandoned since 2020. Expect things to break. Feel free to fork and keep building**


**Read the complete documentation here: https://pyforkurento.readthedocs.io/en/latest/**


## CHANGELOG <a id = "change"></a>
*This changelog loosely follows semantic versioning*
### 0.1.7 5th Mar 2020
**Improved**
* Streaming speeds by reducing player endpoint latency

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

## PLAN
1. Implement better asynchronocity. Asyncio?
2. Write tests
3. Release V1.0.0
4. Write as many recipes as are in the [official docs](https://doc-kurento.readthedocs.io/en/latest/user/tutorials.html)
