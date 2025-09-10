# 🚂 GetSetRide - Railway Ticket Reservation System

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2.5-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**A modern, beautiful, and responsive railway ticket booking platform built with Django**

[🌟 Features](#-features) • [🚀 Quick Start](#-quick-start) • [📱 Screenshots](#-screenshots) • [🛠️ Tech Stack](#️-tech-stack) • [📄 License](#-license)

</div>

---

## ✨ Features

### 🎨 **Beautiful Modern UI**
- **Glass Morphism Design** - Stunning backdrop-blur effects and transparent elements
- **Gradient Backgrounds** - Eye-catching indigo-to-purple gradient themes
- **Floating Animations** - Smooth, engaging micro-interactions
- **Responsive Design** - Perfect on desktop, tablet, and mobile devices

### 🎫 **Core Functionality**
- **🏠 Home Page** - Stunning landing page with hero section and feature highlights
- **🔍 Train Search** - Advanced search with multiple filters (stations, dates, class)
- **📋 Train Listings** - Beautiful cards showing available trains with details
- **🎫 Ticket Booking** - Streamlined booking process with passenger management
- **💳 Payment Integration** - Secure payment processing interface
- **👤 User Authentication** - Beautiful login and signup pages

### 📱 **User Experience**
- **📞 Contact Support** - Professional contact page with multiple channels
- **ℹ️ Feature Showcase** - Detailed features page highlighting platform benefits
- **🔐 Secure Forms** - Form validation and security measures
- **⚡ Fast Loading** - Optimized performance and smooth transitions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- MySQL or MariaDB installed and running
- Git installed
- Basic knowledge of Django

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lolit-Bairiganjan/TicketReservationSystemWeb.git
   cd TicketReservationSystemWeb
   ```

2. **Navigate to the project directory**
   ```bash
   cd DemoProject
   ```

3. **Install dependencies**
   ```bash
   pip install django mysqlclient
   ```
   
   *Note: For MariaDB, you can also use:*
   ```bash
   pip install django PyMySQL
   ```

4. **Configure database settings**
   Update `DemoProject/settings.py` with your MySQL/MariaDB credentials:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'your_database_name',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

5. **Create database**
   ```bash
   # Login to MySQL/MariaDB and create database
   mysql -u root -p
   CREATE DATABASE your_database_name;
   exit
   ```

6. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Open your browser**
   Navigate to `http://127.0.0.1:8000/` to see the beautiful application!

---

## 📱 Screenshots

<div align="center">

### 🏠 Home Page
*Beautiful hero section with gradient backgrounds and floating animations*

### 🎫 Booking Interface
*Intuitive train search and booking with modern card layouts*

### 📞 Contact Page
*Professional contact form with multiple communication channels*

### 🔐 Authentication
*Stunning login and signup pages with glass morphism effects*

</div>

---

## 🛠️ Tech Stack

### **Backend**
- **Django 5.2.5** - High-level Python web framework
- **Python 3.13** - Programming language
- **MySQL/MariaDB** - Relational database management system
- **mysqlclient/PyMySQL** - Python MySQL database connectors

### **Frontend**
- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first CSS framework
- **JavaScript** - Interactive functionality
- **Google Fonts (Inter)** - Beautiful typography

### **Design Features**
- **Glass Morphism** - Modern backdrop-blur effects
- **Gradient Design System** - Consistent color schemes
- **Responsive Layout** - Mobile-first approach
- **CSS Animations** - Smooth transitions and hover effects

---

## 📁 Project Structure

```
DemoProject/
├── DemoProject/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI configuration
│   └── asgi.py             # ASGI configuration
├── mainApp/
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   │   ├── home.html           # 🏠 Landing page
│   │   ├── features.html       # ✨ Features showcase
│   │   ├── contact.html        # 📞 Contact page
│   │   ├── login.html          # 🔐 User login
│   │   ├── login_signup.html   # 🎉 User registration
│   │   ├── Book_Your_Ticket_Now.html  # 🎫 Booking interface
│   │   ├── available_trains.html      # 🚂 Train listings
│   │   └── payment.html        # 💳 Payment processing
│   ├── views.py            # View functions
│   ├── urls.py             # App URL patterns
│   ├── models.py           # Database models
│   └── admin.py            # Admin configuration
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded files
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies (if present)
```

---

## 🌟 Key Features Breakdown

### 🎨 **Design Excellence**
- **Modern Glass Morphism** - Trendy transparent design elements
- **Gradient Color Schemes** - Professional indigo-to-purple gradients
- **Smooth Animations** - Floating elements and hover effects
- **Typography** - Clean Inter font family for readability

### 🚂 **Railway Booking Features**
- **Multi-class Support** - First AC, Second AC, Third AC, Sleeper, Chair Car
- **Date Selection** - Advanced date picker for journey planning
- **Passenger Management** - Support for up to 6 passengers per booking
- **Real-time Availability** - Dynamic train availability display

### 📱 **Responsive Design**
- **Mobile Optimized** - Perfect experience on all screen sizes
- **Touch Friendly** - Large buttons and touch targets
- **Fast Loading** - Optimized images and CSS
- **Progressive Enhancement** - Works without JavaScript as fallback

---

## 🚀 Getting Started with Development

### **Adding New Features**
1. Create new views in `mainApp/views.py`
2. Add URL patterns in `mainApp/urls.py`
3. Create beautiful templates following the existing design system
4. Use Tailwind CSS classes for consistent styling

### **Customizing Design**
- Modify gradient colors in the CSS custom properties
- Adjust glass morphism effects in the backdrop-blur classes
- Customize animations by modifying the floating-animation keyframes

### **Database Customization**
- Update models in `mainApp/models.py`
- Configure MySQL/MariaDB settings in `DemoProject/settings.py`
- Run `python manage.py makemigrations` and `python manage.py migrate`
- Add admin interface configurations in `mainApp/admin.py`
- For production, consider using connection pooling and optimized settings

---

## 🤝 Contributing

We welcome contributions to make GetSetRide even better! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### **Areas for Contribution**
- 🎨 UI/UX improvements
- 🔧 New features and functionality
- 🐛 Bug fixes and optimizations
- 📚 Documentation enhancements
- 🧪 Test coverage improvements

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Developer

**Lolit Bairiganjan**
- GitHub: [@Lolit-Bairiganjan](https://github.com/Lolit-Bairiganjan)
- Project: [TicketReservationSystemWeb](https://github.com/Lolit-Bairiganjan/TicketReservationSystemWeb)

---

## 🙏 Acknowledgments

- **Django Community** - For the amazing web framework
- **Tailwind CSS** - For the utility-first CSS framework
- **Google Fonts** - For the beautiful Inter typography
- **Open Source Community** - For inspiration and best practices

---

<div align="center">

**⭐ If you found this project helpful, please give it a star! ⭐**

**🚂 Happy Booking with GetSetRide! 🎫**

*Made with ❤️ and Django*

</div>
