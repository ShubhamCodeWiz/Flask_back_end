from market import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
        print("Database tables created.")
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)