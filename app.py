from typing import Any
from flask import Flask
from flask import request
from flask import render_template, redirect
from stories import story, Story
import json

class StoryEncoder(json.JSONEncoder):
  def default(self, o: Any) -> Any:
    if isinstance(o, Story):
      return o.__dict__
    return super().default(o)
  
def load_story_list_from_file(filename='story_list.json'):
  storyList = []
  with open(filename) as f:
    try:
      storyList = json.load(f, object_hook = lambda dictData: Story(words=dictData['prompts'], text=dictData['template']))
    except json.JSONDecodeError:
      storyList = []
  return storyList

def save_story_list_to_file(storyList, filename='story_list.json'):
  with open(filename, 'w') as f:
    json.dump(storyList, f, cls=StoryEncoder)

def add_story(story):
  storyList.append(story)
  save_story_list_to_file(storyList)

app = Flask(__name__)

storyList = load_story_list_from_file()

if len(storyList) == 0:
  add_story(story)

@app.route('/')
def home_page():
  return render_template('home.html', storyList=storyList)

@app.route('/story/<int:storyId>', methods=['POST'])
def story_page(storyId):
  result = storyList[storyId].generate(request.form)
  return render_template('story.html', result=result)

@app.route('/prompt/<int:storyId>')
def prompt_page(storyId):
  return render_template('prompt.html', story = storyList[storyId], storyId=storyId)

@app.route('/new-story')
def new_story_page():
  return render_template('new-story.html')

@app.route('/new-story', methods=['POST'])
def create_story():
  
  words = request.form['words']
  text = request.form['text']

  words = list(map(lambda word: word.lower().strip(),words.split(',')))
  story = Story(words, text)
  add_story(story)
  return redirect('/', code=303)


