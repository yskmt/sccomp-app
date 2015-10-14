# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for, redirect, jsonify


import sys
import os

scc_dir = '/Users/ysakamoto/Projects/sccomp'
sys.path.append(scc_dir)
from os.path import join as opj
from skimage import io
from sccomp import load_gists, load_queries, get_gist, get_matches

gists_db_name = opj(scc_dir, 'dbs/gist_data.npy')
f_db_name = opj(scc_dir, 'dbs/file_names.npy')
data_dir = opj(scc_dir, 'data/scene_database/')
img_dirs = [d for d in os.listdir(data_dir)
            if os.path.isdir(os.path.join(data_dir, d))]
param_name = opj(scc_dir, 'gistparams')




# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form


@app.route('/')
def form():
    return render_template('canvas.html')

# @app.route('/hello/test')
# def test():
#     return "Hello World!"


# @app.route('/hello', methods=["GET"])
# def results(mst, matches):
#     return render_template('results.html', mst=mst, matches=matches)


# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is
# accepting: POST requests in this case
@app.route('/hello', methods=['POST'])
def hello():
    if request.method=='POST':

        mask_name = 'mask.png'
        img_data = request.form['imgBase64'].split('base64,')[1]
        fh = open(mask_name, "wb")
        fh.write(img_data.decode('base64'))
        fh.close()

        gist_data, file_names, param = load_gists(gists_db_name, f_db_name, param_name)
        query_name, img_query, img_files \
            = load_queries(img_dirs, data_dir, 0, mask_name,
                           query_name=request.form['img'].split('/')[-1])

        # img_mask = io.imread(mask_name, as_grey=True)
        img_mask = io.imread(mask_name)
        img_mask = img_mask[:,:,3]
        io.imsave(mask_name, img_mask)
        
        gist, block_weight = get_gist(query_name, img_query, img_mask, param)

        mst_name, _, matches \
            = get_matches(gist, gist_data, block_weight,
                          file_names, img_mask, query_name,
                          mask_name, plot_figure=False, save_dir='static/results')

        return jsonify(mst=mst_name, m0=matches[0], m1=matches[1], m2=matches[2],
                       m3=matches[3], m4=matches[4], m5=matches[5])

    
# Run the app :)
if __name__ == '__main__':
    app.run(debug=True)
        # host="0.0.0.0",
        # port=int("80")
    # )
