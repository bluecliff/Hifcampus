#!/usr/bin/env python
# encoding: utf-8


from flask.ext.script import Manager, Server, Command

from hifcampus import create_app
from hifcampus.models import Hifuser,Id
from werkzeug import generate_password_hash

app = create_app()
manager = Manager(app)

class AddUser(Command):
    '''增加一个用户到用户列表'''
    def run(self):
        user = Hifuser()
        user.nickname='hifcampus'
        user.email='admin@hifcampus.com'
        user.password=generate_password_hash('hifcampus')
        user.id=Id.get_next_id('uid')
	user.roles=[0]
        user.save()
# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0',
    port=8000)
)
manager.add_command('adduser',AddUser)

if __name__ == "__main__":
    print 'start manager'
    manager.run()
