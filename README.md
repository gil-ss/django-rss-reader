# 📰 Django RSS Reader 🐍

![Django Tests](https://github.com/gil-ss/django-rss-reader/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/gil-ss/django-rss-reader/branch/main/graph/badge.svg)](https://codecov.io/gh/gil-ss/django-rss-reader)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Learning%20Project-yellow)

A simple web-based RSS feed reader, built with Django and Python.
This application allows users to subscribe to RSS feeds, view feed items, and manage their subscriptions with ease.

---

### Features

* **User Authentication**: Secure login and registration system.
* **Feed Management**: Add, update, and delete RSS feeds.
* **Feed Parsing**: Parses RSS feeds using `feedparser`.
* **Pagination**: Paginated view of feed items.
* **Responsive UI**: Clean and responsive user interface.
* **Custom Messages**: Success and error messages with customizable colors.

---

### Demo

![Demo](https://github.com/user-attachments/assets/5ef5bde4-dc5d-4b11-a07a-3fda9c7d68c6)
---

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/gil-ss/django-rss-reader.git
   cd django-rss-reader
   ```

2. **Create a virtual environment**:

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

---

### Running Tests

To run the test suite:

```bash
python manage.py test
```
