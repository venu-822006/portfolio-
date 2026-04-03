# KV Reddy Portfolio — Full Stack Setup

## Project Files

```
portfolio.html     ← Frontend (open in browser)
app.py             ← Flask backend
requirements.txt   ← Python dependencies
messages.json      ← Auto-created when first message is sent
```

---

##  How to Run

### Step 1 — Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Start the Flask server
```bash
python app.py
```
You should see:
```
   KV Reddy Portfolio Backend
  Running on  : http://localhost:5000
  Health check: http://localhost:5000/api/health
  Messages    : http://localhost:5000/api/messages
```

### Step 3 — Open the portfolio
Open `portfolio.html` directly in your browser.  
Fill the contact form and hit **Execute Request →**

---

## 🔌 API Endpoints

| Method | Endpoint          | Description                        |
|--------|-------------------|------------------------------------|
| GET    | /api/health       | Check if server is running         |
| POST   | /api/contact      | Submit a contact form message      |
| GET    | /api/messages     | View all received messages (dev)   |

### POST /api/contact — Example
```json
{
  "name":    "Recruiter Name",
  "email":   "hr@company.com",
  "message": "Hi Venu, we'd love to connect!"
}
```

### Success Response
```json
{
  "status":  "success",
  "message": "Thanks Recruiter! Your message has been received.",
  "id":      1
}
```

---

##  Where Messages Are Saved

All messages are stored in `messages.json` in the same folder.  
You can also view them at: `http://localhost:5000/api/messages`

---

##  Before Going Live

- Remove or password-protect the `/api/messages` route
- Set `debug=False` in `app.py`
- Deploy Flask to a cloud server (Render, Railway, or PythonAnywhere — all free tiers available)
- Update the `fetch` URL in `portfolio.html` from `http://localhost:5000` to your live server URL
