# 🛍️ Storefront (Django)

**Duration:** Jun 2025 – Sep 2025  
**Repository:** [GitHub](#)  

A full-featured **E-commerce application** built with **Django & Django REST Framework**, focusing on performance, scalability, and maintainability.  

---

## 🚀 Features

### 🔐 Authentication & Authorization
- Implemented **JWT-based authentication** with **Djoser**.  
- Supported secure login, registration, and user management.  

### 🛒 E-commerce Features
- Product listing with search, filters, and ordering.  
- Shopping cart and order management.  
- Favorites management for authenticated users.  

### ⚡ Performance Optimization & Testing
- Optimized database queries using **`select_related`** and **`prefetch_related`**.  
- Integrated **Redis caching** (running via **Docker**) to accelerate API responses.  
- Profiled SQL queries and response times using **Django Silk** (detecting N+1 queries).  
- Conducted **load & stress testing** with **Locust** to validate system scalability under heavy traffic.  

### ⏳ Background Processing
- Used **Celery** with Redis broker for **asynchronous tasks** such as sending emails.  

### 📊 Monitoring & Debugging
- Configured **Django loggers** for error tracking, performance monitoring, and debugging.  

### ✅ Testing
- Wrote **automated API tests** with **pytest** to ensure reliability and maintainability.  

### 🛠️ Admin Dashboard
- Customized **Django Admin** for managing products, orders, and users efficiently.  

---

## 📦 Tech Stack
- **Backend:** Django, Django REST Framework  
- **Auth:** JWT via Djoser  
- **Caching:** Redis (Dockerized)  
- **Async Tasks:** Celery + Redis broker  
- **Database:** PostgreSQL (or SQLite for dev)  
- **Testing:** Pytest, Locust, Django Silk  
- **Monitoring:** Django loggers  

---

## 📑 Notes
This version focuses on **performance and scalability**:  
- Redis caching improved API response times.  
- Celery enabled background job processing.  
- Silk + Locust ensured the app handles both **query optimization** and **high traffic loads**.  
