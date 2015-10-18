# sccomp-app - scene completion demo

## How to start

gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker -t 120 app:app

## Dependencies

* Flask
* Flask-SocketIO
* gunicorn

## Implementations

http://web.mit.edu/kehinger/www/class/
http://graphics.cs.cmu.edu/projects/scene-completion/

### GIST

* Use my own GIST implementation form the [original GIST paper](http://people.csail.mit.edu/torralba/code/spatialenvelope/).
* Other implementation:
  [Python wrapper](https://github.com/yuichiroTCY/lear-gist-python)
  for [Lear's GIST implementation](http://lear.inrialpes.fr/software).

### Graphcut
http://www.cc.gatech.edu/cpl/projects/graphcuttextures/
* Use the Python implementation:
  [PyMaxFlow](http://pmneila.github.io/PyMaxflow/index.html)

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