This Girder Slicer CLI container uses girder_client to convert between DICOM-RT and VolView state annotations on an item.

To build, use docker in this directory::

    docker build --force-rm -t ghcr.io/girder/girder-volview-dicomrt/worker-volview-dicomrt --platform linux/amd64 .
    docker push ghcr.io/girder/girder-volview-dicomrt/worker-volview-dicomrt

The push requires that you have logged in with `docker login ghcr.io` with a GitHub token as the password.

Although this can be run as a command line, it is more likely to be run from the Girder interface so that the girder-client api url and token are auto-populated.
