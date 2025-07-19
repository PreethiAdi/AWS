from flask import Flask, render_template, request, redirect, url_for, session
import boto3
from botocore.exceptions import ClientError
import random

app = Flask(__name__)
app.secret_key = 'movie-magic-aws'

# ---------------- AWS Setup ----------------
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')

users_table = dynamodb.Table('Users')
bookings_table = dynamodb.Table('Bookings')

SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:123456789012:BookingTopic'  # Replace with your SNS topic ARN

# ---------------- Routes ----------------

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = request.form.get('remember')
        try:
            resp = users_table.get_item(Key={'email': email})
            user = resp.get('Item')
            if user and user['password'] == password:
                session['user'] = email
                if remember:
                    session.permanent = True
                return redirect(url_for('home'))
        except ClientError:
            pass
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        try:
            resp = users_table.get_item(Key={'email': email})
            if resp.get('Item'):
                return render_template('register.html', error="User already exists")
            users_table.put_item(Item={'email': email, 'password': password, 'phone': phone})
            return redirect(url_for('login'))
        except ClientError:
            return render_template('register.html', error="Registration failed")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home1.html')

@app.route('/movies')
def movies_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('movies.html')

@app.route('/book/<int:id>', methods=['GET', 'POST'])
def book_ticket(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    movie_map = {
        1: "Animal", 2: "Devara", 3: "Fidaa", 4: "Inception",
        5: "Orange", 6: "Pushpa", 7: "Remo", 8: "Sakhi"
    }
    movie_name = movie_map.get(id)
    if not movie_name:
        return "Movie not found", 404

    movie = {"id": id, "name": movie_name}

    if request.method == 'POST':
        name = request.form['name']
        try:
            tickets = int(request.form['tickets'])
            email = session['user']
            booking_id = str(random.randint(100000, 999999))

            bookings_table.put_item(Item={
                'booking_id': booking_id,
                'email': email,
                'username': name,
                'movie': movie_name,
                'count': tickets
            })

            message = (
                f"Hi {name},\n\n"
                f"You booked {tickets} ticket(s) for \"{movie_name}\".\n"
                "Enjoy your movie!"
            )
            try:
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject='Movie Booking Confirmation',
                    Message=message
                )
            except ClientError as e:
                print(f"[SNS ERROR] {e}")

            return render_template('success.html', movie=movie, name=name, tickets=tickets)
        except ValueError:
            return render_template('book.html', movie=movie, error="Invalid ticket count")
    return render_template('book.html', movie=movie)

@app.route('/admin')
def admin():
    try:
        resp = bookings_table.scan()
        all_bookings = resp.get('Items', [])
        return render_template('admin.html', bookings=all_bookings)
    except ClientError:
        return "Failed to load bookings", 500

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        try:
            resp = users_table.get_item(Key={'email': email})
            if resp.get('Item'):
                code = random.randint(1000, 9999)
                session['reset_code'] = code
                session['reset_email'] = email
                print(f"[EMAIL SIMULATION] Reset code for {email}: {code}")
                return redirect(url_for('verify_code'))
        except ClientError:
            pass
        return render_template('forgot_password.html', error="Email not registered")
    return render_template('forgot_password.html')

@app.route('/verify-code', methods=['GET', 'POST'])
def verify_code():
    if request.method == 'POST':
        entered = request.form['code']
        if 'reset_code' in session and entered == str(session['reset_code']):
            return redirect(url_for('reset_password'))
        return render_template('verify_code.html', error="Invalid code.")
    return render_template('verify_code.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_pass = request.form['password']
        email = session.get('reset_email')
        try:
            users_table.update_item(
                Key={'email': email},
                UpdateExpression='SET password = :p',
                ExpressionAttributeValues={':p': new_pass}
            )
            session.pop('reset_code', None)
            session.pop('reset_email', None)
            return redirect(url_for('login'))
        except ClientError:
            return "Password reset failed", 500
    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
