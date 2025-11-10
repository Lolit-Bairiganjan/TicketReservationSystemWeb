# Railway Ticket Reservation System

A comprehensive Django-based web application for railway ticket booking and management, featuring real-time seat allocation, berth preference, and PNR tracking.

## 🚂 Features

### User Management
- **User Authentication**: Secure login/logout system with session management
- **User Registration**: New user signup with validation
- **Login Protection**: Restricted access to booking features for authenticated users only

### Ticket Booking System
- **Train Search**: Search trains by route and journey date
- **Schedule Browsing**: View available train schedules with seat availability
- **Multi-Passenger Booking**: Book up to 6 passengers in a single transaction
- **Berth Preference**: Choose preferred berth type (Lower/Middle/Upper/Side Lower/Side Upper)
- **Smart Seat Allocation**: 
  - Automatic seat assignment based on berth type
  - Realistic Indian Railways seat numbering (e.g., Lower: 1,4,7... Middle: 2,5,8... Upper: 3,6,9...)
  - Coach-wise seat tracking (Sleeper, AC 3-Tier, AC 2-Tier, AC 1-Tier)
- **Add Passengers to Existing PNR**: Add more passengers to an already booked ticket under the same PNR
- **Duplicate Prevention**: 
  - Prevents same person from booking multiple tickets on the same train/date
  - Validates duplicate names within a single booking

### PNR Management
- **Unique PNR Generation**: Auto-generated 10-digit PNR for each ticket
- **PNR Status Check**: Real-time ticket and passenger status lookup
- **Comprehensive Ticket Details**: View journey info, passenger list, seat/berth assignments, and fare

### Train & Route Management
- **Multiple Train Types**: Support for Express, Shatabdi, Rajdhani, Duronto, and Garib Rath
- **Station Management**: Pre-populated major Indian railway stations
- **Route Planning**: Define multi-station routes with arrival/departure times
- **Dynamic Fare Calculation**: Per-route fare with base, distance, and class charges

### Coach & Seat Management
- **Coach Types**: Sleeper, AC 3-Tier, AC 2-Tier, AC 1-Tier, First Class
- **Berth Distribution**:
  - **Sleeper/AC 3-Tier**: 72 seats (18 Lower + 18 Middle + 18 Upper + 9 Side Lower + 9 Side Upper)
  - **AC 2-Tier**: 48 seats (16 Lower + 16 Upper + 8 Side Lower + 8 Side Upper)
  - **AC 1-Tier**: 24 seats (12 Lower + 12 Upper - cabin style)
- **Real-time Availability Tracking**: Updates available berths after each booking

### Advanced Features
- **Session Management**: Maintains booking context across pages
- **Transaction Safety**: Atomic database operations for booking integrity
- **Journey Date Validation**: Prevents booking for past dates
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **Admin Panel**: Django admin for data management

## 🛠️ Technology Stack

- **Backend**: Django 5.1.3
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Authentication**: Django built-in authentication system
- **ORM**: Django ORM with complex querysets

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd TicketReservationSystemWeb/DemoProject
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install django
```

4. **Apply migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Seed the database**
```bash
python manage.py seed_data
```

This will populate:
- 8 major railway stations (Delhi, Mumbai, Agra, Jaipur, Kolkata, Chennai, Bangalore, Ahmedabad)
- 5 trains with different types and routes
- Coaches with proper berth distribution
- Train routes with timings
- Fare structures

6. **Create superuser (for admin access)**
```bash
python manage.py createsuperuser
```

7. **Run the development server**
```bash
python manage.py runserver
```

8. **Access the application**
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## 📱 Usage

### Booking a Ticket

1. **Login** or **Register** a new account
2. Click **"Book Your Ticket Now"** on the home page
3. Select **train**, **from/to stations**, and **journey date**
4. View available **schedules** and click **"Book"**
5. Fill passenger details:
   - Name, Age, Gender
   - Seat Class
   - Coach (filtered by class)
   - Berth Preference (optional - auto-assigned if not selected)
6. Submit the form
7. Receive **PNR** and view ticket details

### Adding More Passengers

1. From ticket details page, click **"Add More Passengers"**
2. Fill new passenger details
3. Submit - passengers will be added to the same PNR

### Checking PNR Status

1. Click **"Check PNR Status"** (requires login)
2. Enter **10-digit PNR**
3. View complete ticket and passenger information

## 📊 Database Models

### Core Models
- **Station**: Railway stations with code, name, city, state
- **Train**: Train details with number, name, type, total seats
- **TrainRoute**: Station-wise route with arrival/departure times and sequence
- **TrainSchedule**: Daily train schedules with journey date and status
- **Coach**: Coach details with type, capacity, and berth tracking
- **Fare**: Route-based pricing with base fare, distance charge, and class multiplier
- **Ticket**: Booking record with PNR, schedule, source/destination, total fare
- **Passenger**: Individual passenger details with seat/berth assignment

### Key Relationships
- Train → Coaches (One-to-Many)
- Train → Routes (Many-to-Many through TrainRoute)
- Train → Schedules (One-to-Many)
- Schedule → Tickets (One-to-Many)
- Ticket → Passengers (One-to-Many)

## 🔧 Project Structure

```
DemoProject/
├── mainApp/
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py          # Database seeding script
│   ├── migrations/
│   ├── templates/
│   │   └── mainApp/
│   │       ├── home.html             # Landing page
│   │       ├── login.html            # Login page
│   │       ├── signup.html           # Registration page
│   │       ├── select_destinations.html  # Train search
│   │       ├── schedule_list.html    # Available schedules
│   │       ├── book_ticket.html      # Booking form
│   │       ├── ticket_detail.html    # Ticket view
│   │       └── pnr_status.html       # PNR checker
│   ├── models.py                     # Database models
│   ├── views.py                      # View functions
│   ├── forms.py                      # Form definitions
│   ├── urls.py                       # URL routing
│   └── admin.py                      # Admin configuration
├── DemoProject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
└── manage.py
```

## 🔐 Security Features

- CSRF protection on all forms
- Session-based authentication
- Login required decorators on booking views
- SQL injection prevention via Django ORM
- Password hashing with Django's built-in system

## 🎯 Future Enhancements

- [ ] Payment gateway integration
- [ ] Email/SMS notifications
- [ ] Ticket cancellation with refund
- [ ] Waiting list management
- [ ] User booking history
- [ ] Train live tracking
- [ ] Seat availability calendar view
- [ ] Multi-language support
- [ ] PDF ticket generation
- [ ] RAC (Reservation Against Cancellation) support

## 🐛 Known Issues

- Berth preference may not always be honored if preferred berths are full
- Session data persists until manually cleared - implement auto-cleanup

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 📧 Contact

For questions or support, please contact the development team.

## 🙏 Acknowledgments

- Django documentation
- Indian Railways for inspiration
- Tailwind CSS for styling
- Contributors and testers

---

**Version**: 1.0.0  
**Last Updated**: November 2025