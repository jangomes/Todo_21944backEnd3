# Import necessary modules and libraries
from bson.objectid import ObjectId
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB instance
client = MongoClient('localhost', 27017)
db = client.flask_db
todos = db.todos


# Define root route for index page
@app.route('/', methods=('GET', 'POST'))
def index():
    # If form has been submitted via POST method, extract form data and insert new tod_o item into database
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        new_data = {
            'content': content,
            'degree': degree,
            'completed': False  # add the new "completed" field with a default value
        }
        todos.insert_one(new_data)
        return redirect(url_for('index'))
    # Retrieve all tod_o items from database and pass them to the index.html template for rendering
    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)


# Define route for deleting tod_o items
@app.post('/<id>/delete/')
def delete(id):
    # Delete the specified tod_o item from the database using its ID and redirect to the home page
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))


# Define route for updating tod_o items
#This route takes an id parameter, which corresponds to the ID of the Tod_o item that needs to be updated.
#It first retrieves the Tod_o item from the database using this ID, and then renders an update form with the current values pre-filled.
# When the form is submitted, it updates the Tod_o item in the database and redirects to the home page
@app.route('/<id>/update/', methods=('GET', 'POST'))
def update(id):
    # Retrieve the specified tod_o item from the database using its ID
    todo = todos.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        # If form has been submitted via POST method, extract form data and update the tod_o item in the database
        content = request.form['content']
        degree = request.form['degree']
        completed = request.form.get('completed', False) == 'Yes'
        todos.update_one({"_id": ObjectId(id)}, {"$set": {"content": content, "degree": degree, "completed": completed}})
        return redirect(url_for('index'))

    # Pass the tod_o item data to the update.html template for rendering
    return render_template('update.html', todo=todo)


# Define route for creating a new tod_o item
@app.route('/create', methods=['POST'])
def create_todo():
    content = request.form['content']
    degree = request.form['degree']
    due_date = request.form['due_date']
    todos.insert_one({'content': content, 'degree': degree, 'due_date': due_date})
    return redirect(url_for('index'))
