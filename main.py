import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Todo

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Todo': Todo}


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)