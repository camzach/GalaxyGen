import GalaxyGen
import BalancedGalaxy
import os
from io import BytesIO
from random import sample
from flask import Flask, send_file, current_app, request, redirect
app = Flask(__name__)

GalaxyGen.init(app.root_path)
BalancedGalaxy.init(app.root_path)

@app.route('/')
def hello_world():
  return 'Hello World!'
  
@app.route('/galaxy')
def galaxy():
  return current_app.send_static_file('galaxy.html')

@app.route('/galaxy/generate')
def generate():
  size = request.args.get('size', default = 1, type = int)
  mode = request.args.get('mode', default = 'random')
  tiles = request.args.get('tiles')
  if mode == 'random':
    systems = list(map(lambda x: str(x), sample(range(19, 51), 30)))
  if mode == 'tiles':
    systems = tiles.split(',')
  if mode == 'balanced':
    systems = ','.join(BalancedGalaxy.generateBalancedGalaxy())
    return '/galaxy/generate?mode=tiles&tiles=' + systems + '&size=' + str(size)
  galaxy = GalaxyGen.genGalaxy(systems, size)
  byte_io = BytesIO()
  galaxy.save(byte_io, 'PNG')
  byte_io.seek(0)
  return send_file(byte_io, mimetype='image/png')

@app.route('/galaxy/fullrandom')
def fullrandom():
  size = request.args.get('size', default = 1, type = int)
  systems = sample([str(x) for x in range(19, 51)], 30)
  galaxy = GalaxyGen.genGalaxy(systems, size)
  byte_io = BytesIO()
  galaxy.save(byte_io, 'PNG')
  byte_io.seek(0)
  return send_file(byte_io, mimetype='image/png')

if __name__ == '__main__':
  app.run()
