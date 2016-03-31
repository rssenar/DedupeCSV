
from flask import Flask

app = Flask(__name__) # create the application object

app.config["DEBUG"] = True

@app.route('/')
@app.route('/hello')

def hello_world():
	return 'The Quick Brown Fox Jumpped Over The Lazy Dog'

# dynamic route
@app.route('/test/<search_query>')
def search(search_query):
	return search_query

@app.route("/name/<name>")
def index(name):
	if name.lower() == "michael" :
		return 'Hello, {}'.format(name), 200
	else:
		return "Name Not Found", 404

if __name__ == "__main__":
	app.run()
