from app import app
from fake_data import generate_fake_users, generate_fake_jobs, generate_fake_applications

if __name__ == "__main__":
    with app.app_context():
        generate_fake_users()
        generate_fake_jobs()
        generate_fake_applications()

    app.run(debug=True)
