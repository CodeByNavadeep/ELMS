from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms import LeaveForm, RegisterForm
from flask_sqlalchemy import SQLAlchemy
from extensions import db  
from models import Leave, User 
from functools import wraps
import pandas as pd

app = Flask(__name__)
app.secret_key = "@navadeep$12345"

login_manager = LoginManager()
login_manager.login_view = 'login'  # redirect here if not logged in
login_manager.init_app(app)

#Database config (SQLite)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///elms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# Initialize DB
db.init_app(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already exists. Choose another!", "warning")
            return render_template("register.html", form=form)

        # Create new user
        new_user = User(
            username=form.username.data,
            password=form.password.data,  
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))


    return render_template("register.html", form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash(f"Welcome, {user.username}!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))


def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in allowed_roles:
                flash("You are not authorized to access this page.", "danger")
                return redirect(url_for('login'))  
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/apply', methods=["GET", "POST"])
@login_required
@role_required(['Employee'])
def apply():
    form=LeaveForm()
    if form.validate_on_submit():
        new_leave = Leave(
            reason=form.reason.data,
            from_date=form.from_date.data,
            to_date=form.to_date.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_leave)
        db.session.commit()
        flash("Leave application submitted and saved!", "success")
        return redirect(url_for('apply'))
    return render_template("apply.html", form=form)


@app.route('/leave-history', methods=['GET', 'POST'])
@login_required
@role_required('Employee')
def leave_history():
    query = Leave.query.filter_by(user_id=current_user.id)

    status_filter = request.args.get('status')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    if status_filter and status_filter != "All":
        query = query.filter_by(status=status_filter)

    if from_date:
        query = query.filter(Leave.from_date >= from_date)

    if to_date:
        query = query.filter(Leave.to_date <= to_date)

    leaves = query.order_by(Leave.from_date.desc()).all()
    return render_template("leave_history.html", leaves=leaves)

@app.route('/leave/edit/<int:leave_id>', methods=['GET', 'POST'])
@login_required
@role_required('Employee')
def edit_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)

    # Allow only the owner and if still pending
    if leave.user_id != current_user.id or leave.status != "Pending":
        flash("You are not allowed to edit this leave.", "danger")
        return redirect(url_for('leave_history'))

    form = LeaveForm(obj=leave)

    if form.validate_on_submit():
        leave.reason = form.reason.data
        leave.from_date = form.from_date.data
        leave.to_date = form.to_date.data
        leave.description = form.description.data
        db.session.commit()
        flash("Leave updated successfully!", "success")
        return redirect(url_for('leave_history'))

    return render_template("edit_leave.html", form=form)

@app.route('/leave/cancel/<int:leave_id>')
@login_required
@role_required('Employee')
def cancel_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)

    if leave.user_id != current_user.id or leave.status != "Pending":
        flash("You are not allowed to cancel this leave.", "danger")
        return redirect(url_for('leave_history'))

    db.session.delete(leave)
    db.session.commit()
    flash("Leave canceled successfully.", "info")
    return redirect(url_for('leave_history'))


@app.route('/dashboard/manager')
@login_required
@role_required(['Manager'])
def manager_dashboard():
    query = Leave.query  # Managers see all leaves

    status_filter = request.args.get('status')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    if status_filter and status_filter != "All":
        query = query.filter_by(status=status_filter)

    if from_date:
        query = query.filter(Leave.from_date >= from_date)

    if to_date:
        query = query.filter(Leave.to_date <= to_date)

    leaves = query.order_by(Leave.from_date.desc()).all()
    return render_template("manager_dashboard.html", leaves=leaves)

@app.route('/dashboard/employee')
@login_required
@role_required(['Employee'])
def employee_dashboard():
    return render_template("employee_dashboard.html")

@app.route('/dashboard/admin')
@login_required
@role_required(['Admin'])
def admin_dashboard():
    users = User.query.all()
    leaves = Leave.query.all()
    return render_template("admin_dashboard.html", users=users, leaves=leaves)

@app.route('/download/csv')
@login_required
@role_required(['Admin'])
def download_csv():
    leaves = Leave.query.all()
    data = []

    for leave in leaves:
        data.append({
            'Employee': leave.user.username,
            'Reason': leave.reason,
            'From Date': leave.from_date,
            'To Date': leave.to_date,
            'Status': leave.status
        })

    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)

    response = make_response(csv_data)
    response.headers['Content-Disposition'] = 'attachment; filename=leave_report.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response


@app.route('/leave/approve/<int:leave_id>')
@login_required
@role_required(['Manager'])
def approve_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    leave.status = 'Approved'
    db.session.commit()
    flash("Leave approved successfully!", "success")
    return redirect(url_for('manager_dashboard'))

@app.route('/leave/reject/<int:leave_id>')
@login_required
@role_required(['Manager'])
def reject_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    leave.status = 'Rejected'
    db.session.commit()
    flash("Leave rejected.", "warning")
    return redirect(url_for('manager_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)