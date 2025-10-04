""" from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import re

# Flask app setup
app = Flask(__name__)
app.secret_key = "super_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xls', 'xlsx'}

# Database setup
db = SQLAlchemy(app)

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

# ----------------------- Models -----------------------
class FinancialData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    expenses = db.Column(db.Float, nullable=False)
    net_profit = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<FinancialData {self.company_name}>"

    def calculate_net_profit(self):
        self.net_profit = self.revenue - self.expenses


# ----------------------- Utility Class -----------------------
class FileProcessor:

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    @staticmethod
    def is_valid_company_name(name):
        return re.match(r"^[A-Za-z0-9\s\.\-&]+$", name)

    @classmethod
    def process_file(cls, filepath):
        try:
            if filepath.endswith('.csv'):
                data = pd.read_csv(filepath)
            else:
                data = pd.read_excel(filepath)

            data.columns = data.columns.str.lower().str.replace(" ", "_")
            required_cols = {"company_name", "revenue", "expenses"}

            if not required_cols.issubset(data.columns):
                raise ValueError("Missing required columns: company_name, revenue, expenses.")

            for _, row in data.iterrows():
                name = str(row["company_name"]).strip()
                revenue = float(row["revenue"])
                expenses = float(row["expenses"])

                if not cls.is_valid_company_name(name):
                    raise ValueError(f"Invalid company name: {name}")

                report = FinancialData(company_name=name, revenue=revenue, expenses=expenses)
                report.calculate_net_profit()
                db.session.add(report)

            db.session.commit()
            cls.generate_visualizations()

        except Exception as e:
            flash(f"Error processing file: {str(e)}", "error")
            db.session.rollback()

    @staticmethod
    def generate_visualizations():
        records = FinancialData.query.all()
        if not records:
            return

        names = [r.company_name for r in records]
        revenues = [r.revenue for r in records]
        expenses = [r.expenses for r in records]
        profits = [r.net_profit for r in records]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(names, revenues, label="Revenue", color="blue")
        ax.bar(names, expenses, label="Expenses", color="red", alpha=0.7)
        ax.bar(names, profits, label="Net Profit", color="green", alpha=0.7)
        ax.set_xlabel("Companies")
        ax.set_ylabel("Amount")
        ax.set_title("Financial Overview")
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        chart_path = os.path.join("static", "financial_chart.png")
        plt.savefig(chart_path)
        plt.close()


# ----------------------- Routes -----------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        try:
            file = request.files['file']
            if file and FileProcessor.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                FileProcessor.process_file(filepath)
                flash("File uploaded and processed successfully!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid file type.", "error")
        except Exception as e:
            flash(f"Unexpected error: {str(e)}", "error")
    return render_template("upload.html")

@app.route("/dashboard")
def dashboard():
    reports = FinancialData.query.all()
    return render_template("dashboard.html", reports=reports)


# ----------------------- Run App -----------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all() """



from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import re

# Flask app setup
app = Flask(__name__)
app.secret_key = "super_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xls', 'xlsx'}

# Database setup
db = SQLAlchemy(app)

# Create necessary folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

# ----------------------- Models -----------------------
class FinancialData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    revenue = db.Column(db.Float, nullable=False)
    expenses = db.Column(db.Float, nullable=False)
    net_profit = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<FinancialData {self.company_name}>"

    def calculate_net_profit(self):
        self.__net_profit = self.revenue - self.expenses


# ----------------------- Utility Class -----------------------
class FileProcessor:

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

    @staticmethod
    def is_valid_company_name(name):
        return re.match(r"^[A-Za-z0-9\s\.\-&]+$", name)

    @classmethod
    def process_file(cls, filepath):
        try:
            if filepath.endswith('.csv'):
                data = pd.read_csv(filepath)
            else:
                data = pd.read_excel(filepath)

            data.columns = data.columns.str.lower().str.replace(" ", "_")
            required_cols = {"company_name", "revenue", "expenses"}

            if not required_cols.issubset(data.columns):
                raise ValueError("Missing required columns: company_name, revenue, expenses.")

            for _, row in data.iterrows():
                name = str(row["company_name"]).strip()
                revenue = float(row["revenue"])
                expenses = float(row["expenses"])

                if not cls.is_valid_company_name(name):
                    raise ValueError(f"Invalid company name: {name}")

                report = FinancialData(company_name=name, revenue=revenue, expenses=expenses)
                report.calculate_net_profit()
                db.session.add(report)
                

            db.session.commit()
            cls.generate_visualizations()

        except Exception as e:
            flash(f"Error processing file: {str(e)}", "error")
            db.session.rollback()

    @staticmethod
    def generate_visualizations():
        records = FinancialData.query.all()
        if not records:
            return

        names = [r.company_name for r in records]
        revenues = [r.revenue for r in records]
        expenses = [r.expenses for r in records]
        profits = [r.net_profit for r in records]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(names, revenues, label="Revenue", color="blue")
        ax.bar(names, expenses, label="Expenses", color="red", alpha=0.7)
        ax.bar(names, profits, label="Net Profit", color="green", alpha=0.7)
        ax.set_xlabel("Companies")
        ax.set_ylabel("Amount")
        ax.set_title("Financial Overview")
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        chart_path = os.path.join("static", "financial_chart.png")
        plt.savefig(chart_path)
        plt.close()


# ----------------------- Routes -----------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        try:
            file = request.files['file']
            if file and FileProcessor.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                FileProcessor.process_file(filepath)
                flash("File uploaded and processed successfully!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid file type.", "error")
        except Exception as e:
            flash(f"Unexpected error: {str(e)}", "error")
    return render_template("upload.html")

@app.route("/dashboard")
def dashboard():
    reports = FinancialData.query.all()
    return render_template("dashboard.html", reports=reports)


# ----------------------- Run App -----------------------
if __name__ == "__main__":
    with app.app_context():
        print("[DEBUG] Creating database...")
        db.create_all()
        print("[DEBUG] Done creating tables.")
    print("DB path:", os.path.abspath("database.db"))
    app.run(debug=True)
