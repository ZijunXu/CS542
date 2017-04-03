from api_server import app

@app.before_first_request
def create_tables():
	db.create_all()


if __name__ == "__main__":
    from api_server import db
    db.init_app(app)
    app.run()
