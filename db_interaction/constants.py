from werkzeug.security import generate_password_hash


ADMIN_PASSWORD = generate_password_hash('password123')  # no ability to enter password from interface now
CATEGORIES = ('арифметика', '1', '2', '3')
SCORES = ('10', '20', '30', '40')
