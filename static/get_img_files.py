import os
import os.path
from os.path import join


base = '/Users/ysakamoto/Projects/post_action'
base_s = join(base, 'static')
base_ss = join(base_s, 'scene_database')

structure = {}
for d in os.listdir(base_ss):

    imfls = {}
    dd = join(base_ss, d)
    if os.path.isdir(dd):
        for imf in os.listdir(dd):
            if 'jpg' in imf:
                imfls[imf.split('.jpg')[0]] = join('static', 'scene_database', d, imf)

        structure[d] = imfls
    

import json
with open('img_files.json', 'w') as f:
    f.write(json.dumps(structure))
