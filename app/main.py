import sqlite3
import psycopg2
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort


def get_db_connection():
    conn = psycopg2.connect(dbname='test1', user='postgres', password='Aa12345', host='localhost')
    conn.autocommit = True#    return conn
    cursor = conn.cursor()
    return cursor


def get_post(post_id):
    conn = get_db_connection()
    conn.execute('SELECT * FROM posts WHERE id = %s', (post_id,))
    post = conn.fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


@app.route('/')
def index():
    conn = get_db_connection()
    print(conn, type(conn))
    conn.execute('SELECT * FROM posts')
    posts = conn.fetchall()
    print("\n\nposts=",posts)
    print("\n\n")
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (%s, %s)',(title, content))
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = %s, content = %s WHERE id = %s',(title, content, id))
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = %s', (id,))
    conn.close()
    flash('"{}" was successfully deleted!'.format(post[2]))
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
 app.run(host="0.0.0.0")