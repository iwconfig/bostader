from flask import Flask, abort
import traceback, importlib, sys, os

def load(_):
  try:
    if _ in sys.modules:
      return importlib.reload(sys.modules[_])
    else:
      return importlib.import_module(_)
  except BaseException:
    traceback.print_exc()
    abort(500, description='error error! something is wrong')

app = Flask('app')

@app.route('/')
def hello_world():
  return '''
  <a href="./hb">Hudiksvallsbostäder</a>
  <br>
  <a href="./nb">Nordanstigsborstäder</a>
  <br>
  <a href="./gh">Gotlandshem</a>
  '''

@app.route('/hb.html')
@app.route('/hb/html')
@app.route('/hudiksvallsbostäder.html')
@app.route('/hudiksvallsbostäder/html')
def hudiksvallsbostäder_html():
  hb = load('hudiksvallsbostäder')
  resp = app.make_response(hb.df.to_html())
  resp.mimetype = "text/html"
  return resp

@app.route('/hb')
@app.route('/hb.txt')
@app.route('/hb/txt')
@app.route('/hudiksvallsbostäder')
@app.route('/hudiksvallsbostäder.txt')
@app.route('/hudiksvallsbostäder/txt')
def hudiksvallsbostäder_text():
  hb = load('hudiksvallsbostäder')
  resp = app.make_response(hb.df.to_string())
  resp.mimetype = "text/plain"
  return resp

@app.route('/nb.html')
@app.route('/nb/html')
@app.route('/nordanstigsbostäder.html')
@app.route('/nordanstigsbostäder/html')
def nordanstigsbostäder_html():
  hb = load('nordanstigsbostäder')
  resp = app.make_response(hb.df.to_html())
  resp.mimetype = "text/html"
  return resp

@app.route('/nb')
@app.route('/nb.txt')
@app.route('/nb/txt')
@app.route('/nordanstigsbostäder')
@app.route('/nordanstigsbostäder.txt')
@app.route('/nordanstigsbostäder/txt')
def nordanstigsbostäder_text():
  hb = load('nordanstigsbostäder')
  resp = app.make_response(hb.df.to_string())
  resp.mimetype = "text/plain"
  return resp


@app.route('/gh.html')
@app.route('/gh/html')
@app.route('/gotlandshem.html')
@app.route('/gotlandshem/html')
def gotlandshem_html():
  hb = load('gotlandshem')
  resp = app.make_response(hb.df.to_html())
  resp.mimetype = "text/html"
  return resp

@app.route('/gh')
@app.route('/gh.txt')
@app.route('/gh/txt')
@app.route('/gotlandshem')
@app.route('/gotlandshem.txt')
@app.route('/gotlandshem/txt')
def gotlandshem_text():
  hb = load('gotlandshem')
  resp = app.make_response(hb.df.to_string())
  resp.mimetype = "text/plain"
  return resp


#app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
  port = os.environ.get('PORT')
  #port = 8080
  if not port:
    raise Exception('PORT environment variable is not set')
  app.run(host='0.0.0.0', port=int(port))
