import sqlite3

from markdown import markdown
from flask import Flask, render_template,  Markup

app = Flask(__name__)


def curs():
    db = sqlite3.connect('jobs_git.db')
    return db.cursor()


@app.route('/')
def get_jobs():
    c = curs()
    jobs = c.execute('SELECT numb, name FROM jobs').fetchall()

    return render_template('home.html', jobs=jobs)


@app.route('/<issues>')
def issue_info(issues):
    c = curs()
    content = c.execute('SELECT name, content FROM jobs WHERE numb=?',
                        [int(issues)]).fetchone()

    issue_name = content[0]
    issue_content = Markup(markdown(content[1]))

    return render_template('content.html',
                           name=issue_name,
                           content=issue_content
                           )


def main():
    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()
