"""
app.py

Demo to show the scene completion algorithm.

"""

import sys
import os
import time
from os.path import join as opj

from gevent import monkey
monkey.patch_all()

from threading import Thread
from flask import (Flask, render_template, session, request, url_for,
                   redirect, jsonify)
from flask.ext.socketio import SocketIO, emit, join_room, leave_room, \
    close_room, disconnect

from skimage import io
from src.sccomp import (load_gists, load_queries, get_gist,
                        get_matches, mask_complete, scene_complete)


# Globals
scc_dir = 'static/data'
gists_db_name = opj(scc_dir, 'dbs/gist_data.npy')
f_db_name = opj(scc_dir, 'dbs/file_names.npy')
data_dir = opj(scc_dir, 'scene_database/')
img_dirs = [d for d in os.listdir(data_dir)
            if os.path.isdir(os.path.join(data_dir, d))]
param_name = opj(scc_dir, 'gistparams')

# Initialize the Flask/SocketIO application
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('canvas.html')

# Get the mask image from socketio and send back the completed image
# urls
@socketio.on('mask image', namespace='/scc')
def calculate(message):
    if message['type'] == 'POST':

        mask_name = 'mask.png'
        # img_data = request.form['imgBase64'].split('base64,')[1]
        img_data = message['data']['imgBase64'].split('base64,')[1]
        
        fh = open(mask_name, "wb")
        fh.write(img_data.decode('base64'))
        fh.close()

        print "loading database..."
        gist_data, file_names, param = load_gists(gists_db_name, f_db_name, param_name)
        
        print "loading queries..."
        query_name, img_query, img_files \
            = load_queries(img_dirs, data_dir, 0, mask_name,
                           query_name=message['data']['img'].split('/')[-1])
                           # query_name=request.form['img'].split('/')[-1])

        print "saving mask image..."
        img_mask = io.imread(mask_name, as_grey=True)
        img_mask = io.imread(mask_name)
        img_mask = img_mask[:,:,3]
        io.imsave(mask_name, img_mask)
        
        print "calculating gist of the query..."
        gist, block_weight = get_gist(query_name, img_query, img_mask, param)

        print "calculating the match and blending..."
        matches, img_mask, img_target \
            = get_matches(gist, gist_data, block_weight,
                          file_names, img_mask, query_name,
                          mask_name, plot_figure=False, save_dir='static/results')

        # mst_name = mask_complete(img_mask, img_target, query_name, save_dir='')
        # print '\nMasked image:', mst_name
        mst_name = ''

        print '\nCompleted images from 1st to 5th choices:'
        sc_names = []
        for i in range(len(matches)):
            sc_names.append(scene_complete(matches[i],
                                           img_mask, img_target,
                                           query_name,
                                           save_dir='static/results/'))
            print sc_names[-1]
            emit('completed image url', {'img_url': sc_names[-1],
                                         'status': len(matches)-i})


@socketio.on('connect', namespace='/scc')
def test_connect():
    emit('app response', {'data': 'Connected', 'count': 0})

@socketio.on('app event', namespace='/scc')
def test_message(message):
    print message['data']
    emit('app response',
         {'data': message['data']})

    
# Run the app :)
if __name__ == '__main__':
    socketio.run(app)
        # host="0.0.0.0",
        # port=int("80")
    # )
