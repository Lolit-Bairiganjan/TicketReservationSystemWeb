PPT: https://www.canva.com/design/DAG42-E3bcA/H1DW535HU7l6e0mcWtJA0A/edit?utm_content=DAG42-E3bcA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

<div align="center">

# 🚂 Railway Ticket Reservation System

### *Your Journey Begins Here* ✨

[![Django](https://img.shields.io/badge/Django-5.1.3-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![MariaDB](https://img.shields.io/badge/MariaDB-10.5+-003545?style=for-the-badge&logo=mariadb&logoColor=white)](https://mariadb.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

*A comprehensive, feature-rich Django web application for seamless railway ticket booking and management*

[Features](#-features) • [Installation](#-installation) • [Database Setup](#-database-configuration) • [Usage](#-usage-guide) • [Contributing](#-contributing)

---

![Railway Booking Banner](https://via.placeholder.com/1200x400/667eea/ffffff?text=GetSetRide+-+Your+Journey+Awaits)

</div>

## 🌟 Overview

Welcome to **GetSetRide** - A modern, full-featured railway ticket reservation system built with Django and MySQL/MariaDB. Experience the convenience of online railway booking with intelligent seat allocation, real-time availability tracking, and comprehensive journey management.

<div align="center">

### 🎯 *Book • Track • Manage* - All in One Place

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 👤 User Management
- 🔐 **Secure Authentication**
  - Login/Logout with session management
  - Password encryption & validation
  - CSRF protection
- 📝 **User Registration**
  - Quick signup process
  - Form validation
- 🛡️ **Access Control**
  - Login-protected booking system
  - Decorator-based route protection

</td>
<td width="50%">

### 🎫 Ticket Booking
- 🔍 **Smart Search**
  - Search by route & date
  - Real-time availability
  - Dynamic schedule display
- 👥 **Multi-Passenger Booking**
  - Book up to 6 passengers
  - Group booking support
  - Individual passenger details
- 🪑 **Berth Preference**
  - Lower/Middle/Upper berths
  - Side berth options
  - Auto-assignment algorithm

</td>
</tr>
<tr>
<td width="50%">

### 🎯 Smart Seat Allocation
- 🤖 **Intelligent Assignment**
  - Automated seat allocation
  - Berth-type based numbering
  - Coach-wise distribution
- 📊 **Real-time Tracking**
  - Live seat availability
  - Coach-wise monitoring
  - Berth availability per coach
- ✅ **Validation**
  - Duplicate booking prevention
  - Same-person check
  - Capacity constraints

</td>
<td width="50%">

### 📱 PNR Management
- 🔢 **Unique PNR Generation**
  - 10-digit alphanumeric PNR
  - Auto-generation on booking
  - Collision detection
- 🔎 **Status Check**
  - Real-time PNR lookup
  - Complete journey information
  - Passenger details display
- ➕ **Add Passengers**
  - Add to existing PNR
  - Same journey extension
  - Dynamic fare calculation

</td>
</tr>
</table>

---

## 🛠️ Technology Stack

<div align="center">

### *Built with Modern Technologies*

<table>
<tr>
<td align="center" width="20%">
<img src="https://www.djangoproject.com/m/img/logos/django-logo-negative.png" width="100" alt="Django"/><br/>
<b>Django 5.1.3</b><br/>
<sub>Backend Framework</sub>
</td>
<td align="center" width="20%">
<img src="https://www.python.org/static/community_logos/python-logo.png" width="100" alt="Python"/><br/>
<b>Python 3.8+</b><br/>
<sub>Programming Language</sub>
</td>
<td align="center" width="20%">
<img src="https://www.mysql.com/common/logos/logo-mysql-170x115.png" width="100" alt="MySQL"/><br/>
<b>MySQL 8.0+</b><br/>
<sub>Database</sub>
</td>
<td align="center" width="20%">
<img src="https://mariadb.com/wp-content/uploads/2019/11/mariadb-logo-vert_blue-transparent.png" width="100" alt="MariaDB"/><br/>
<b>MariaDB 10.5+</b><br/>
<sub>Alternative DB</sub>
</td>
<td align="center" width="20%">
<img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/Tailwind_CSS_Logo.svg" width="100" alt="Tailwind"/><br/>
<b>Tailwind CSS</b><br/>
<sub>Styling Framework</sub>
</td>
</tr>
</table>

**Additional Technologies:**
- 🔌 **mysqlclient** - Python MySQL database connector
- 🎨 **HTML5/CSS3** - Frontend markup and styling
- ⚡ **JavaScript** - Interactive features
- 🔐 **Django Auth** - Security and authentication
- 📊 **Django ORM** - Database abstraction layer

</div>

---

## 📋 Prerequisites

<div align="center">

```bash
✅ Python 3.8 or higher
✅ MySQL 8.0+ OR MariaDB 10.5+
✅ pip (Python package manager)
✅ Virtual environment (recommended)
✅ Git (for cloning)
```

</div>

---

## 🚀 Installation

<div align="center">

### *Get Started in 5 Minutes!* ⚡

</div>

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/railway-reservation-system.git
cd railway-reservation-system/DemoProject
```

### 2️⃣ Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
# Install Django
pip install django

# Install MySQL connector
pip install mysqlclient

# If mysqlclient installation fails, try:
# For Ubuntu/Debian:
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

# For Fedora/Red Hat:
sudo dnf install python3-devel mysql-devel

# For macOS:
brew install mysql-client
export PATH="/usr/local/opt/mysql-client/bin:$PATH"

# Then retry:
pip install mysqlclient
```

### 4️⃣ Database Configuration

#### Option A: MySQL Setup

```bash
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE railway_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Create user and grant privileges
CREATE USER 'railway_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON railway_db.* TO 'railway_user'@'localhost';
FLUSH PRIVILEGES;

# Exit MySQL
EXIT;
```

#### Option B: MariaDB Setup

```bash
# Login to MariaDB
mariadb -u root -p

# Create database
CREATE DATABASE railway_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Create user and grant privileges
CREATE USER 'railway_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON railway_db.* TO 'railway_user'@'localhost';
FLUSH PRIVILEGES;

# Exit MariaDB
EXIT;
```

### 5️⃣ Configure Django Settings

Update the database configuration in `DemoProject/settings.py`:

```python
# filepath: DemoProject/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway_db',
        'USER': 'railway_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',   # Or your database server IP
        'PORT': '3306',        # Default MySQL/MariaDB port
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

<details>
<summary><b>🔒 Security Best Practice: Using Environment Variables</b></summary>

Instead of hardcoding credentials, use environment variables:

```python
# filepath: DemoProject/settings.py

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'railway_db'),
        'USER': os.environ.get('DB_USER', 'railway_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

Create a `.env` file:
```bash
DB_NAME=railway_db
DB_USER=railway_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306
```

Install python-decouple:
```bash
pip install python-decouple
```

</details>

### 6️⃣ Run Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Verify migrations
python manage.py showmigrations
```

### 7️⃣ Populate Sample Data

```bash
# Run the seed command to populate database
python manage.py seed_data
```

<details>
<summary><b>📦 What gets seeded?</b></summary>

- ✅ **8 Major Indian Railway Stations**
  - Mumbai Central (MUM)
  - New Delhi (DEL)
  - Kolkata (KOL)
  - Chennai Central (CHN)
  - Bengaluru (BLR)
  - Hyderabad (HYD)
  - Agra Cantt (AGR)
  - Jaipur Junction (JP)

- ✅ **5 Trains** with different types
  - Rajdhani Express
  - Shatabdi Express
  - Duronto Express
  - InterCity Express
  - Superfast Express

- ✅ **40+ Coaches** with proper berth distribution
  - Sleeper Class (72 seats each)
  - AC 3-Tier (64 seats each)
  - AC 2-Tier (48 seats each)
  - AC 1-Tier (24 seats each)
  - General (100 seats each)
  - First Class (32 seats each)

- ✅ **Train Routes** with intermediate stations
- ✅ **Fare Structures** for all routes
- ✅ **Sample Schedules** for next 7 days

</details>

### 8️⃣ Create Admin User

```bash
python manage.py createsuperuser

# Follow the prompts:
# Username: admin
# Email: admin@railway.com
# Password: (enter secure password)
# Password (again): (confirm password)
```

### 9️⃣ Launch the Server

```bash
python manage.py runserver

# Server will start at http://127.0.0.1:8000/
```

### 🔟 Access the Application

<div align="center">

| Service | URL | Description |
|---------|-----|-------------|
| 🌐 **Main Site** | http://127.0.0.1:8000/ | User Interface |
| 🔧 **Admin Panel** | http://127.0.0.1:8000/admin/ | Management Console |

**Default Admin Credentials:**
- Username: `admin`
- Password: (what you set in step 8)

</div>

---

## 🔧 Database Configuration Options

<div align="center">

### MySQL/MariaDB Advanced Settings

</div>

### Connection Pool Settings

For production environments, configure connection pooling:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway_db',
        'USER': 'railway_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'connect_timeout': 10,
        },
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

### Database Performance Optimization

```sql
-- For MySQL
SET GLOBAL max_connections = 200;
SET GLOBAL innodb_buffer_pool_size = 2G;
SET GLOBAL query_cache_size = 64M;

-- For MariaDB
SET GLOBAL max_connections = 200;
SET GLOBAL innodb_buffer_pool_size = 2G;
```

### Backup and Restore

```bash
# Backup database
mysqldump -u railway_user -p railway_db > railway_db_backup.sql

# Restore database
mysql -u railway_user -p railway_db < railway_db_backup.sql
```

---

## 📊 Database Models

<div align="center">

### *Database Architecture*

</div>

### Core Models

| Model | Purpose | Key Fields | Database Type |
|-------|---------|------------|---------------|
| 🏢 **Station** | Railway stations | Code, Name, City, State | VARCHAR, TEXT |
| 🚂 **Train** | Train information | Number, Name, Type, Total Seats | VARCHAR, INT |
| 🗺️ **TrainRoute** | Station routes | Train, Station, Timing, Sequence | FK, TIME, INT |
| 📅 **TrainSchedule** | Daily schedules | Train, Journey Date, Status, Base Fare | FK, DATE, DECIMAL(8,2) |
| 🚃 **Coach** | Coach details | Type, Capacity, Berth tracking | VARCHAR, INT |
| 💰 **Fare** | Pricing | Base, Distance, Charges | DECIMAL(8,2), INT |
| 🎫 **Ticket** | Bookings | PNR, Schedule, Source, Destination, Total Fare | CHAR(10), FK, DECIMAL(10,2) |
| 👤 **Passenger** | Traveler info | Name, Age, Seat, Berth, Status, Fare | VARCHAR, INT, DECIMAL(10,2) |

### Important Field Types

```sql
-- PNR: Unique 10-character alphanumeric
pnr VARCHAR(10) UNIQUE NOT NULL

-- Decimal precision for money
total_fare DECIMAL(10, 2)
base_fare DECIMAL(8, 2)

-- DateTime with timezone
booking_date DATETIME DEFAULT CURRENT_TIMESTAMP

-- Check constraints
CONSTRAINT available_seats_not_exceed_total 
  CHECK (available_seats <= total_seats)
```

### Database Relationships

```
Station ──┐
          ├──> TrainRoute ──> Train ──┐
Station ──┘                           ├──> TrainSchedule ──> Ticket ──> Passenger
                                      │                          │
                             Coach ───┘                          └──> Payment
                                                                      Fare ──┘
```

---

## 🔍 Common Database Issues & Solutions

<div align="center">

| Issue | Solution |
|-------|----------|
| ❌ `Access denied for user` | Check username/password in settings.py |
| ❌ `Can't connect to MySQL server` | Ensure MySQL/MariaDB is running: `sudo systemctl status mysql` |
| ❌ `Unknown database 'railway_db'` | Create database: `CREATE DATABASE railway_db;` |
| ❌ `mysqlclient installation failed` | Install dev packages: `sudo apt-get install libmysqlclient-dev` |
| ❌ `OperationalError: Lost connection` | Increase timeout: `'connect_timeout': 30` in OPTIONS |
| ❌ `Incorrect string value` | Use utf8mb4 charset in database and connection |

</div>

### Troubleshooting Commands

```bash
# Check MySQL/MariaDB status
sudo systemctl status mysql     # or mariadb

# Restart database server
sudo systemctl restart mysql    # or mariadb

# Check database connection
mysql -u railway_user -p railway_db -e "SELECT 1;"

# View Django database migrations
python manage.py showmigrations

# Reset migrations (CAUTION: Deletes data!)
python manage.py migrate mainApp zero
python manage.py migrate
```

---

## 📱 Usage Guide

[Rest of the README remains the same as the previous version, starting from Usage Guide section...]

---

## 🌐 Production Deployment Tips

### MySQL/MariaDB for Production

```python
# Production database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'railway_db_prod',
        'USER': 'railway_prod_user',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'your-database-server.com',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'ssl': {'ca': '/path/to/ca-cert.pem'},  # Enable SSL
        },
        'CONN_MAX_AGE': 600,
        'ATOMIC_REQUESTS': True,
    }
}
```

### Performance Recommendations

- ✅ Enable MySQL query cache
- ✅ Use connection pooling (CONN_MAX_AGE)
- ✅ Add database indexes on frequently queried fields
- ✅ Enable slow query log for optimization
- ✅ Regular database backups (automated)
- ✅ Monitor connection pool usage
- ✅ Use read replicas for scaling

---

<div align="center">

## ⭐ Star this Repository

*If you find this project helpful, please consider giving it a star!*

[![GitHub stars](https://img.shields.io/github/stars/yourusername/railway-reservation-system?style=social)](https://github.com/yourusername/railway-reservation-system)

---

### 🚂 *Happy Journey with GetSetRide!* ✨

**Version**: 1.0.0 | **Last Updated**: January 2025 | **Database**: MySQL/MariaDB

Made with ❤️ by the GetSetRide Team

---

[⬆ Back to Top](#-railway-ticket-reservation-system)

</div>
