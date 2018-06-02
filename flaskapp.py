import GalaxyGen
import os
from io import BytesIO
from random import sample
from flask import Flask, send_file
app = Flask(__name__)

GalaxyGen.setpath(app.root_path)

@app.route('/')
def hello_world():
  return 'Hello World!'

@app.route('/galaxy/generate/')
def help():
  return 'Please add a comma-delimited list of tile numbers to the URL.'

@app.route('/galaxy/generate/<tiles>')
def generate(tiles):
  systems = tiles.split(',')
  galaxy = GalaxyGen.genGalaxy(systems)
  byte_io = BytesIO()
  galaxy.save(byte_io, 'PNG')
  byte_io.seek(0)
  return send_file(byte_io, mimetype='image/png')

@app.route('/galaxy/fullrandom')
def fullrandom():
  systems = list(map(lambda x: str(x), sample(range(19, 51), 30)))
  galaxy = GalaxyGen.genGalaxy(systems)
  byte_io = BytesIO()
  galaxy.save(byte_io, 'PNG')
  byte_io.seek(0)
  return send_file(byte_io, mimetype='image/png')

if __name__ == '__main__':
  app.run()
