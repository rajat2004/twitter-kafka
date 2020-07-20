from flask import Flask, render_template
app = Flask(__name__)

# Home page, which has links to topic pages
@app.route('/')
def home():
    return render_template('home.html')

# Each topic has text file created in the root directory
@app.route('/topic/<name>')
def display_topic_file(name):
    with open(f'../{name}', 'r') as f:
        return render_template('content.html', content=f.read())

if __name__ == '__main__':
  app.run(host='0.0.0.0')
