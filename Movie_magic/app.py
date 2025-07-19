from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'movie-magic-local'

# ------------------ In-Memory Storage ------------------
users = []
bookings = []

# ------------------ Movie List ------------------
# UPDATED: Using your provided movie images with proper URLs
movies = [
    {
        "id": 1, 
        "name": "Orange", 
        "time": "6:00 PM - 9:00 PM", 
        "price": 200, 
        "rating": 4.0, 
        "image": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/orange.jpg-9u6xwilqx3WmtJIauwfMKyKSKSxxDp.jpeg",
        "genre": "Romance/Drama",
        "year": 2010,
        "description": "A romantic drama about love, sacrifice, and second chances."
    },
    {
        "id": 2, 
        "name": "Varsham", 
        "time": "7:30 PM - 10:30 PM", 
        "price": 190, 
        "rating": 4.5, 
        "image": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/varsham.jpg-Spg8kHXfoSVU4wZtLXuq6ft7W944yx.jpeg",
        "genre": "Romance/Drama",
        "year": 2004,
        "description": "A classic romantic drama that became a milestone in Telugu cinema."
    },
    {
        "id": 3, 
        "name": "Arya 2", 
        "time": "8:00 PM - 11:00 PM", 
        "price": 240, 
        "rating": 4.3, 
        "image": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/arya.jpg-Pm5cczKozDlz1Eq5ExifjPtGIGxsC0.jpeg",
        "genre": "Romance/Action",
        "year": 2009,
        "description": "A romantic action film about unconditional love and friendship."
    },
    {
        "id": 4, 
        "name": "Inception", 
        "time": "6:30 PM - 9:30 PM", 
        "price": 300, 
        "rating": 4.8, 
        "image": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/inception.jpg-skB3m1xgj3RN9aSa6pZt7gL0qwSojM.jpeg",
        "genre": "Sci-Fi/Thriller",
        "year": 2010,
        "description": "A mind-bending thriller about dream infiltration and reality manipulation."
    },
    {
        "id": 5, 
        "name": "VIP", 
        "time": "5:00 PM - 8:00 PM", 
        "price": 250, 
        "rating": 4.2, 
        "image": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/vip.jpg-sqSfx3WrzzZKDx2PehK0casuMliaoc.jpeg",
        "genre": "Romance/Drama",
        "year": 2014,
        "description": "A heartwarming story about an aspiring engineer and his journey to success."
    },
    {
        "id": 6, 
        "name": "Dear Comrade", 
        "time": "9:00 PM - 12:00 AM", 
        "price": 220, 
        "rating": 4.1, 
        "image": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/dear%20comrade.jpg-30QPDGJRfLibBkU6UkBmDA4XvPEF0g.jpeg",
        "genre": "Romance/Drama",
        "year": 2019,
        "description": "A passionate love story that explores the complexities of relationships."
    },
    {
        "id": 7, 
        "name": "Three", 
        "time": "4:00 PM - 7:00 PM", 
        "price": 180, 
        "rating": 3.8, 
        "image": "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/three.jpg-ZiMQnQWz4CrrARliAR9eyREv8L3ZoL.jpeg",
        "genre": "Romance/Drama",
        "year": 2012,
        "description": "A beautiful tale of love and relationships with emotional depth."
    }
]

@app.route('/')
def index():
    return redirect(url_for('login'))

# ---------------- Login ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = request.form.get('remember')
        
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        if user:
            session['user'] = email
            if remember:
                session.permanent = True
            return redirect(url_for('home'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

# ---------------- Register ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        
        if any(u['email'] == email for u in users):
            return render_template('register.html', error="User already exists")
        
        users.append({
            'email': email,
            'password': password,
            'phone': phone
        })
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ---------------- Home ----------------
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home1.html')

# ---------------- Movies ----------------
@app.route('/movies')
def movies_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('q', '')
    if query:
        filtered = [m for m in movies if query.lower() in m['name'].lower() or query.lower() in m['genre'].lower()]
    else:
        filtered = movies
    return render_template('movies.html', movies=filtered)

# ---------------- Booking ----------------
@app.route('/book/<int:id>', methods=['GET', 'POST'])
def book_ticket(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    movie = next((m for m in movies if m['id'] == id), None)
    if not movie:
        return "Movie not found", 404
    
    if request.method == 'POST':
        name = request.form['name']
        try:
            tickets = int(request.form['tickets'])
            email = session['user']
            booking_id = str(random.randint(100000, 999999))
            
            total_price = movie['price'] * tickets
            
            bookings.append({
                'booking_id': booking_id,
                'email': email,
                'username': name,
                'movie': movie['name'],
                'count': tickets,
                'total_price': total_price
            })
            
            print(f"[EMAIL SIMULATION] Sent booking confirmation to {email}")
            print(f"Hi {name}, You booked {tickets} ticket(s) for {movie['name']}. Total: ₹{total_price}. Enjoy your movie!")
            
            return render_template("success.html", movie=movie, name=name, tickets=tickets, total_price=total_price)
        except ValueError:
            return render_template("book.html", movie=movie, error="Invalid ticket count")
    
    return render_template("book.html", movie=movie)

# ---------------- Admin ----------------
@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('admin.html', bookings=bookings, movies=movies)

# ---------------- Contact Us ----------------
@app.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        print(f"[CONTACT FORM] From: {name} ({email})")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        
        return render_template('contact_us.html', success="Thank you for your message! We will get back to you soon.")
    
    return render_template('contact_us.html')

# ---------------- Help ----------------
@app.route('/help')
def help_page():
    return render_template('help.html')

# ---------------- Forgot Password ----------------
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        user = next((u for u in users if u['email'] == email), None)
        if user:
            code = random.randint(1000, 9999)
            session['reset_code'] = code
            session['reset_email'] = email
            print(f"[EMAIL SIMULATION] Sent reset code to {email}: {code}")
            return redirect(url_for('verify_code'))
        return render_template("forgot_password.html", error="Email not registered")
    return render_template("forgot_password.html")

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
        user = next((u for u in users if u['email'] == email), None)
        if user:
            user['password'] = new_pass
        session.pop('reset_code', None)
        session.pop('reset_email', None)
        return redirect(url_for('login'))
    return render_template('reset_password.html')

# ---------------- Run ----------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
