# sccomp-app - scene completion demo

## How to start

gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker -t 120 app:app

## Dependencies

* Flask
* Flask-SocketIO
    - http://flask-socketio.readthedocs.org/en/latest/
    - http://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent
* gunicorn

## Implementations

* General algorithm of the scene completion is from the paper,
  ["Scene Completion Using Millions of Photographs"](http://graphics.cs.cmu.edu/projects/scene-completion/)
  by Hays and Efros.
* Calculation of GIST descriptor is based on the MATLAB code from the
GIST paper,
[Modeling the shape of the scene: a holistic representation of the spatial envelope](http://people.csail.mit.edu/torralba/code/spatialenvelope/)
by Oliva and Torralba.
* Poisson image blending is based on the algorithm described in the
  paper,
  ["Poisson Image Editing"](https://www.cs.jhu.edu/~misha/Fall07/Papers/Perez03.pdf)
  by Perez, Gangnet and Blake.
* Graphcut algorithm will be implemented.


## Dataset

* Used
["8 Scene Categories Dataset"](http://people.csail.mit.edu/torralba/code/spatialenvelope/spatial_envelope_256x256_static_8outdoorcategories.zip),
which consists of 2600 color images with 256x256 pixels.

## TODO

1. Implement the edge case for Poisson blending.
2. Implement graphcut algorithm:
    - http://www.cc.gatech.edu/cpl/projects/graphcuttextures/
    - Use the Python implementation?:
      [PyMaxFlow](http://pmneila.github.io/PyMaxflow/index.html)
3. Speed up - use Cython for Poisson blending?
4. User larger dataset.
5. Better handling of errors.


<!---
## Google image search
http://incandescent.xyz/docs/
https://www.imageraider.com
https://github.com/vivithemage/mrisa
https://www.mashape.com/imagesearcher/camfind#!documentation
http://cloudsightapi.com/api
-->

## Datasets

### Urban and Natural Scene Categories
http://cvcl.mit.edu/database.htm

<!---
http://vision.cs.princeton.edu/projects/2010/SUN/
http://groups.csail.mit.edu/vision/TinyImages/


# Etc

## git submodules document
http://git-scm.com/book/en/v2/Git-Tools-Submodules
-->
