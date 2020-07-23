from flask import Flask, render_template
from os.path import dirname, abspath

app = Flask(__name__)

# Home page, which has links to topic pages
@app.route('/')
def home():
    return render_template('home.html')

# Each topic has text file created in the root/outputs directory
@app.route('/topic/<name>')
def display_topic_file(name):
    # Root directory
    d = dirname(dirname(abspath(__file__)))
    filename = f'{d}/outputs/{name}'

    with open(filename, 'r') as f:
        return render_template('content.html', content=f.read())

if __name__ == '__main__':
  app.run(host='0.0.0.0')
