\# Movie Magic - Flask Movie Booking Application



A simple movie booking application built with Flask.



\## Features



\- User registration and login

\- Password reset functionality

\- Movie browsing and search

\- Ticket booking

\- Admin panel for viewing bookings

\- Responsive design



\## Setup Instructions



1\. \*\*Install Python\*\* (3.7 or higher)



2\. \*\*Clone or download this project\*\*



3\. \*\*Install dependencies:\*\*

&nbsp;  \\`\\`\\`bash

&nbsp;  pip install -r requirements.txt

&nbsp;  \\`\\`\\`



4\. \*\*Run the application:\*\*

&nbsp;  \\`\\`\\`bash

&nbsp;  python app.py

&nbsp;  \\`\\`\\`



5\. \*\*Open your browser and go to:\*\*

&nbsp;  \\`\\`\\`

&nbsp;  http://localhost:5000

&nbsp;  \\`\\`\\`



\## Project Structure



\\`\\`\\`

flask-movie-booking/

├── app.py                 # Main Flask application

├── requirements.txt       # Python dependencies

├── README.md             # This file

├── templates/            # HTML templates

│   ├── login.html

│   ├── register.html

│   ├── home1.html

│   ├── movies.html

│   ├── book.html

│   ├── success.html

│   ├── admin.html

│   ├── forgot\_password.html

│   ├── verify\_code.html

│   └── reset\_password.html

└── static/               # Static files (CSS, images)

&nbsp;   ├── css/

&nbsp;   │   ├── styles.css    # Login/form styles

&nbsp;   │   ├── home.css      # Home page styles

&nbsp;   │   ├── movies.css    # Movies page styles

&nbsp;   │   └── admin.css     # Admin page styles

&nbsp;   └── images/

&nbsp;       └── movie\_bg.jpg  # Background image

\\`\\`\\`



\## Usage



1\. \*\*Register a new account\*\* or use existing credentials

2\. \*\*Browse movies\*\* on the movies page

3\. \*\*Book tickets\*\* by clicking "Book Now"

4\. \*\*View bookings\*\* in the admin panel

5\. \*\*Use forgot password\*\* feature if needed



\## Default Test Data



The application comes with 8 sample movies pre-loaded for testing.



\## Notes



\- This is a development version with in-memory storage

\- All data is lost when the server restarts

\- Email notifications are simulated in the console

\- For production use, implement proper database storage and email services



