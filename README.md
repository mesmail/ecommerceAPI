# Django REST Framework - E-commerce API

This project is a **RESTful API** for a simple **e-commerce system** built using **Django REST Framework (DRF)**.  
It supports **user authentication, product management, order processing, performance optimization, and security best practices**.  

---

## 🚀 Features Implemented
✅ **User Authentication & Authorization**  
- JWT-based authentication (Login, Register, Token Refresh)  
- Permissions: **Only Admins** can create/update/delete products  
- Users can only view **their own orders**  

✅ **Product Management**  
- CRUD operations for products (**Admin-only for Create, Update, Delete**)  
- Search & Filtering: Search by **name** and **category**  
- Pagination: 20 products per page  

✅ **Order Processing**  
- Users can place orders (**stock is validated before purchase**)  
- Atomic transactions to prevent stock race conditions  
- **Idempotency Key** to prevent duplicate orders  

✅ **Performance Optimization**  
- `select_related` & `prefetch_related` to optimize database queries  
- **Pagination (20 products per page)** for scalability  
- **Redis caching** for faster responses  

✅ **Security Enhancements**  
- Protection against **SQL Injection & XSS**  
- Validation & sanitization of all user inputs  
- **Idempotency Keys** for preventing duplicate order submissions  

---

## ⚙️ Installation & Setup

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/ecommerce-api.git
cd ecommerce-api
