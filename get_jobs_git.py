import requests
import sqlite3


def jobs_table():
    with sqlite3.connect('jobs_git.db') as db:
        c = db.cursor()

        c.execute('drop table if exists jobs')
        c.execute('create table jobs (numb, name, content)')

        page = 1
        while True:
            resp = requests.get('https://api.github.com/repos/awesome-'
                                'jobs/vietnam/issues?page={}'.format(page))
            data = resp.json()
            result = []

            if not data:
                break
            else:
                for job_info in data:
                    result.append((job_info['number'],
                                   job_info['title'],
                                   job_info['body']))
            page += 1
            c.executemany('insert into jobs values (?, ?, ?)', result)


def main():
    jobs_table()


if __name__ == '__main__':
    main()
