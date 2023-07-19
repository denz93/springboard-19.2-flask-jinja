from flask import Flask
from flask import request
from flask import render_template
from stories import story

app = Flask(__name__)

@app.route('/')
def home_page():
  return render_template('home.html', prompts=story.prompts)

@app.route('/story', methods=['POST'])
def story_page():
  result = story.generate(request.form)
  return render_template('story.html', result=result)
