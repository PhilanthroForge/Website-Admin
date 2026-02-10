# PhilanthroForge Admin Panel

## Quick Start

### 1. Setup
```bash
cd admin
chmod +x setup.sh
./setup.sh
```

### 2. Run
```bash
source venv/bin/activate
python3 app.py
```

### 3. Access
- URL: http://localhost:5000/admin
- Email: `admin@philanthroforge.com`
- Password: `ChangeMe123!`

**⚠️ Change the password immediately after first login!**

---

## Features

### ✅ Completed (Phase 1)
- Secure login with bcrypt password hashing
- Session management with auto-logout
- Admin dashboard with stats
- Image browser (view folders and images)
- Settings page (password change)

### 🚧 In Progress
- Page content editor with WYSIWYG
- Image upload functionality
- Component editor (nav/footer)
- Services/Case Studies CMS

---

## Project Structure

```
admin/
├── app.py                  # Main Flask application
├── auth.py                 # Authentication logic
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── setup.sh               # Setup script
├── users.db               # SQLite database (created on first run)
├── templates/             # HTML templates
│   ├── base.html
│   └── admin/
│       ├── login.html
│       ├── dashboard.html
│       ├── pages.html
│       ├── images.html
│       └── settings.html
└── data/                  # Content storage (JSON files)
    ├── pages/
    ├── services/
    ├── case-studies/
    └── components/
```

---

## Security Features

- **Password Hashing**: Bcrypt with cost factor 12
- **Session Management**: HTTP-only cookies, 30-min timeout
- **CSRF Protection**: Built into Flask forms
- **Login Required**: All admin routes protected

---

## Next Development Phases

1. **Content Editor** - WYSIWYG editor for page content
2. **Image Manager** - Upload, rename, delete images
3. **Component Editor** - Edit nav/footer visually
4. **Services CMS** - Full CRUD for services
5. **Case Studies CMS** - Full CRUD for case studies

---

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

### Database Issues
```bash
# Reset database
rm users.db
# Run app again to recreate
python3 app.py
```

### Dependencies Issues
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```
