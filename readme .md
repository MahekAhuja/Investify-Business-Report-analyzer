# 📊 Investify – Business Tax Report Analyzer

A **Flask-based web application** that helps businesses analyze their financial data by uploading reports (CSV/Excel).  
It automatically calculates **Revenue, Expenses, Net Profit**, and generates **visualizations** for better insights.

---

## 🚀 Features
- 📂 Upload financial reports (`.csv`, `.xls`, `.xlsx`)
- 🔎 Automatic parsing & validation of company names and columns
- 🧮 Calculates **Net Profit = Revenue – Expenses**
- 📊 Interactive **Dashboard** displaying company-wise results
- 📈 Auto-generated financial charts using **Matplotlib**
- 💾 Stores financial data in **SQLite Database**
- ⚡ Simple, clean UI built with **Flask Templates**

---

## 🛠️ Tech Stack
- **Backend:** Flask, SQLAlchemy, Python
- **Frontend:** HTML, Jinja2 Templates, CSS (via `static/`)
- **Database:** SQLite
- **Libraries:** Pandas, Matplotlib, Regex

---

## 📂 Project Structure
Business_tax_project/
│── instance/ # Database instance folder
│── static/ # Static files (charts, CSS, etc.)
│── templates/ # HTML templates
│ │── base.html
│ │── index.html
│ │── upload.html
│ │── dashboard.html
│── uploads/ # Uploaded CSV/Excel files
│── app.py # Main Flask application
│── README.md # Project documentation