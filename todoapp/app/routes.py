from flask import jsonify, request,session,render_template, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from app import app
from app.models import Todo
from app.models import User
from app.pro_license import Prolicense
from app import db
from flask import render
import bcrypt
import secrets

app.secret_key = secrets.token_urlsafe(100)
login_manager = LoginManager()
login_manager.init_app(app)

# Create routes

# Generete session token
def generate_refresh_token():
    return secrets.token_urlsafe(100)

# Generate refresh token
def generate_refresh_token():
    return secrets.token_urlsafe(100)

def  validate_session_token(session_token):
    if 'session_expire' in session and session['session_expire'] > datetime.datetime.now():
        return True
    else:
        return False
    
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@ app.route('/register',methods=['POST'])
def user_login():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Check user existed or not
    existedUser = User.objects('username')
    existedEmail = User.objects('email')
    if existedUser or existedEmail:
        return jsonify({'error':'Username or email already exists'}),404
    
    # bcrypt password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    
    new_user = User(username=username,email=email,password=hashed_password)

    new_user.save()

    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login',methods = ['POST'])
def user_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.objects(username=username).first()

    if user and bcrypt.checkpw(password.encode('utf-8'),user.password):
        return jsonify({'message':'Login sucessfully'}),201
    else:
        return jsonify({'error':'Invalid username or password'}),404
    
@app.route('/logout')
def user_logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/todos',methods=['GET'])
@login_required
def get_todos(todo):
    todos = Todo.query.all()
    todo_list = [{'id':todo.id,
                  'title':todo.title,
                  'description':todo.description,
                  'createdAt':todo.CreatedAt.strftime('%Y-%m-%d %H:%M:%S'),
                  'updatedAt': todo.updatedAt.strftime('%Y-%m-%d %H:%M:%S')}
                  if Prolicense.purchase == True:
                    'image' : todo.image,
                  else:
                    return jsonify ({'message':'Image can only upload pro-users'})
                  for todo in todos]
    
    return jsonify(todo_list)


@app.route('/todos',methods = ['POST'])
@login_required
def todo_creation():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    createdAt = data.get('createdAt')
    updatedAt = data.get('updatedAt')

    if not title or not description or not createdAt or not updatedAt:
        return jsonify({'Error':'Title,description and time are required'}),400
    
    newTodo = Todo(title=title,description=description,createdAt=createdAt,updatedAt=updatedAt)

    db.session.add(newTodo)
    db.session.commit()

    return jsonify({'message':'Todo created sucessfully ','id':newTodo.id}),200

@app.route('/todos/<int:todo_id>',methods=['GET'])
@login_required
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'Error':'Todo not found'}),404
    
    todo_data = {'id':todo.id,'title':todo.title,'description':todo.description,'createdAt':todo.createdAt,'updatedAt':todo.updatedAt}
    return jsonify(todo_data)


@app.route('/todos/<int:todo_id>',methods=['PUT'])
@login_required
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'Error':'Todo not found'}),404
    
    data = request.json
    title = data.get('title')
    description = data.get('description')
    createdAt = data.get('createdAt')
    updatedAt = data.get('updatedAt')

    if title:
        todo.title = title
    if description:
        todo.description = description
    if createdAt:
        todo.createdAt = createdAt
    if updatedAt:
        todo.updatedAt = updatedAt
    
    db.session.commit()

    return jsonify({'error':'Todo updated sucessfully'}),200


@app.route('/todos/<int:todo_id>',methods = ['DELETE'])
@login_required
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({'error':'Todo not found'}),404
    
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message':'Todo deleted sucessfully'}),200


@app.route('/todo/<int:todo_id>/prchase_pro_license',methods=['GET'])
def prchase_pro_license(todo_id):
    pro_license = Prolicense()

    pro_license.purchase()

    return jsonify({'message':'Pro license purchased sucessfully'}),200



