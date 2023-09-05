from flask import Flask, render_template, request, redirect, url_for, session
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace 'your_secret_key' with a secure secret key

# Database connection
db = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='blog_db'  # Make sure to use the correct database name
)



@app.route('/')
def index():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()

        return redirect(url_for('login'))

    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = username
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' in session:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        return render_template('home.html', posts=posts)
    else:
        return redirect(url_for('login'))
    

    

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        # Process the form data and create a new blog post in the database
        # Replace the following code with your logic to create a new post
        title = request.form['title']
        content = request.form['content']
        
        cursor = db.cursor()
        # Assuming you have an 'author' column in your 'posts' table, add the author's username
        author = session['username']
        cursor.execute("INSERT INTO posts (title, content, author) VALUES (%s, %s, %s)", (title, content, author))
        db.commit()
        
        return redirect(url_for('home'))
    
    return render_template('create_post.html')

@app.route('/my_posts')
def my_posts():
    if 'username' in session:
        # Retrieve the current user's posts from the database
        cursor = db.cursor()
        username = session['username']
        cursor.execute("SELECT * FROM posts WHERE author = %s", (username,))
        posts = cursor.fetchall()
        return render_template('my_posts.html', posts=posts)
    else:
        return redirect(url_for('login'))

@app.route('/post/<int:post_id>')
def post(post_id):
    # This view function should handle displaying individual blog posts.
    # You should implement the logic to fetch and display the post based on the post_id.
    # For now, we'll use a placeholder value.
    
    post_data = {
        'title': 'Sample Blog Post Title',
        'date': 'January 1, 2023',
        'content': 'This is a sample blog post content. Replace this with actual post data.'
    }

    return render_template('post.html', post_title=post_data['title'], post_date=post_data['date'], post_content=post_data['content'])

@app.route('/my_posts')
def my_blog_history():
    if 'username' in session:
        username = session['username']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM posts WHERE author = %s", (username,))
        posts = cursor.fetchall()
        return render_template('my_blog_history.html', posts=posts)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
