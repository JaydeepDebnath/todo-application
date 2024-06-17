import json
from flask import jsonify
from app.models import Todo
import stripe

stripe.api_key = 'https://api.stripe.com/v1/payment_intents'


class Prolicense:
    def __init__(self):
        self.is_purchased = False

    def purchase(self):
        self.is_purchased = True

class TodoApp:
    def __init__(self):
        self.todos = []
        self.pro_license = Prolicense()

    def add_todo(self,title,description,image=None ):
        if not self.pro_license.is_purchased and image:
            return jsonify({'You need to purchase pro license yo upload a image.'}),404
        todo = Todo(title,description,image)
        self.todos.append(todo)

    def list_todo(self):
        for index,todo in enumerate(self.todos,start=1):
            return jsonify({f"{index}.Title:{todo.title},Description:{todo.description},Completed:{todo.completed}"})

    def mark_completed_todo(self,index):
        todo = self.todos[index-1]
        todo.mark_completed_todo()

    def purchase_pro_lisence(self):
        try:
           intent = stripe.PaymentIntent.create(
               amount=1999,
               currency=['USD','INR'],
               payment_method_types=['card'],
               description='Pro lisence purchase'
           )
           return jsonify({'Pro lisence purchased sucessfully'})
        except Exception as e:
            return jsonify({f"Error occured while purchasing pro license:{str(e)}"})
    

def main():
    todo_app = TodoApp

    todo_app.add_todo("Todos")
    todo_app.add_todo("Finish project", "Complete documentation", "project_image.jpg")

    # Initial todos
    todo_app.list_todo()

    # Mark as complete

    todo_app.mark_completed_todo(1)

    # List all todos after markig complete

    todo_app.list_todo()

    # purchase pro license

    todo_app.purchase_pro_lisence()

if __name__=='__main__':
    main()



