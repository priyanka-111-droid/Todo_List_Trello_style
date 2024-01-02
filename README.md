# To do List Website(Trello style)

# To run
```
pip install -r requirements.txt
python main.py
```

# Features
- Login and Register
- Validation for login and register
- View and update User Profile
- Kanban style board(like Trello) with HTML Drag and Drop API(can drag items from 'todo' column to 'doing' column etc)
- Error handling(404 and 500)
- Ability to add todo items, edit each item and delete items.


# To add:
- Deadlines for todo
- List view with deadlines sorted in descending order.
- Testing
- Deployment


# Approach

- Inspired by : https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

- In routes.py, edit route and delete route were referred from https://blog.devgenius.io/how-to-create-a-todo-application-with-flask-21b71651c7dc.


# Learnings

- Importance of virtual env - venv
- NoSQL databases better if less defined structure
- Relational databases(SQL databases) better for blogs,lists etc.
- SQLAlchemy package is an ORM.ORM lets you use classes and objects instead of tables and SQL.
- Alembic is database migration framework for SQLAlchemy.
- Foeign key references primary key of another table.
- One user writes many posts-> One-to-many relationship.
- Error handling using `set FLASK_DEBUG=1` and then custom error pages(@errorhandler decorator)
- Traditional server-side model vs Single Page Applications(SPA) and AJAX
