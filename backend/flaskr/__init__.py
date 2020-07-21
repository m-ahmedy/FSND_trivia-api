import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from utils import paginate_result, format_questions, format_categories

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  cors = CORS(app, resources={r'/*': { 'origins': '*' }})

  @app.after_request
  def allow_cors(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH, OPTIONS')
    return response

  @app.route('/')
  def index():
    return jsonify({
      'success': 'true'
    }), 200

  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    categories = Category.query.all()
    response = {
      'categories': format_categories(categories),
      'success': True
    }
    return jsonify(response)

  @app.route('/questions', methods=['GET'])
  def get_all_questions():
    questions = Question.query.all()
    categories = Category.query.all()
    paginated_result = paginate_result(request, format_questions(questions), QUESTIONS_PER_PAGE)
    response = {
      'success': True,
      'questions': paginated_result,
      'total_questions': len(questions),
      'categories': format_categories(categories),
      'current_category': categories[0].format()
    }
    return jsonify(response)
  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_questions_by_category(id):
    categories = Category.query.all()
    selected_category = Category.query.filter(Category.id == id).one_or_none()
    questions = Question.query.filter(Question.category == selected_category.id).all()
    paginated_result = paginate_result(request, format_questions(questions))
    response = {
      'success': True,
      'questions': paginated_result,
      'total_questions': len(questions),
      'current_category': selected_category.format()
    }
    return jsonify(response)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    