# usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from cube64_2 import *

app = Flask(__name__)

cube_chaine = [3,1,2,1,1,3,1,2,1,2,1,2,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,2,3,1,1,1,3,1,2,1,1,1,1,1,1,1,1,1,3,1]
cube = cube64(cube_chaine)
coord_cube = cube.get_coordonnees()

@app.route('/etat_cube', methods=['GET'])
def get_etat_cube():
    return jsonify(str(coord_cube))

if __name__ == '__main__':
    app.run(debug=True)
