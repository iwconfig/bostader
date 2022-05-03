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

def make_a_element(text, href=None):
  if text and href:
    return f'<a target="_blank" href="{href}">{text}</a>'
  return text

app = Flask('app')

style_html = '<link rel="stylesheet" href="/static/style.css">'

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
  hb.df['Adress'] = hb.df.apply(
    lambda x: make_a_element(x['Adress'], x['Detaljsida']), axis=1
  )
  html = style_html
  html += hb.df.to_html(
    render_links=True,
    escape=False,
  )
  resp = app.make_response(html)
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
  resp = app.make_response(
    hb.df.loc[:, ~hb.df.columns.isin(['Detaljsida'])].to_string() #skippa detaljsida
  )
  resp.mimetype = "text/plain"
  return resp

@app.route('/nb.html')
@app.route('/nb/html')
@app.route('/nordanstigsbostäder.html')
@app.route('/nordanstigsbostäder/html')
def nordanstigsbostäder_html():
  nb = load('nordanstigsbostäder')
  nb.df['Adress'] = nb.df.apply(
    lambda x: make_a_element(x['Adress'], x['Detaljsida']), axis=1
  )
  html = style_html
  html += nb.df.to_html(
    render_links=True,
    escape=False,
  )
  resp = app.make_response(html)
  resp.mimetype = "text/html"
  return resp

@app.route('/nb')
@app.route('/nb.txt')
@app.route('/nb/txt')
@app.route('/nordanstigsbostäder')
@app.route('/nordanstigsbostäder.txt')
@app.route('/nordanstigsbostäder/txt')
def nordanstigsbostäder_text():
  nb = load('nordanstigsbostäder')
  resp = app.make_response(
    nb.df.loc[:, ~nb.df.columns.isin(['Detaljsida'])].to_string() #skippa detaljsida
  )
  resp.mimetype = "text/plain"
  return resp


@app.route('/gh.html')
@app.route('/gh/html')
@app.route('/gotlandshem.html')
@app.route('/gotlandshem/html')
def gotlandshem_html():
  gh = load('gotlandshem')
  gh.df['Adress'] = gh.df.apply(
    lambda x: make_a_element(x['Adress'], x['Detaljsida']), axis=1
  )
  html = style_html
  html += gh.df.to_html(
    render_links=True,
    escape=False,
  )
  resp = app.make_response(html)
  resp.mimetype = "text/html"
  return resp

@app.route('/gh')
@app.route('/gh.txt')
@app.route('/gh/txt')
@app.route('/gotlandshem')
@app.route('/gotlandshem.txt')
@app.route('/gotlandshem/txt')
def gotlandshem_text():
  gh = load('gotlandshem')
  resp = app.make_response(
    gh.df.loc[:, ~gh.df.columns.isin(['Detaljsida'])].to_string() #skippa detaljsida
  )
  resp.mimetype = "text/plain"
  return resp


#app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
  debug = True
  port = os.environ.get('PORT')
  #port = 8080
  if not port:
    raise Exception('PORT environment variable is not set')
  app.run(host='0.0.0.0', port=int(port), debug=debug)
