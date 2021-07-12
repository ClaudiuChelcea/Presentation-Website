from flask import Flask, render_template, request
from flask_mail import Mail, Message

# The webpages are:
# Home: http://127.0.0.1:5000/Index
# Contact: http://127.0.0.1:5000/Contact

# Configure email
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465

# ~~~~~~~~~~~~~~~ INSERT YOUR EMAIL HERE ! ~~~~~~~~~~~~~~~~~
default_email = "any_gmail_dummy@gmail.com"
default_password = "dummy_gmail_password"
app.config['MAIL_USERNAME'] = default_email
app.config['MAIL_PASSWORD'] = default_password

# Display error in console if an email wasn`t inserted
if app.config['MAIL_USERNAME'] == default_email:
    print("\n<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ATTENTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Watch out! For the contact page to submit an email to me correctly, you have to insert \
in the code, as mentioned in the README, a valid email address!");
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ATTENTION >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n")
    print("Website: http://127.0.0.1:5000/Index\n")

# Mail setup
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Index page
@app.route('/Index')
def home():
    meta = {"title": "Home"}
    meta.update({"icon": "https://static.thenounproject.com/png/2048828-200.png"})
    contact_data = {"name": "Chelcea Claudiu", "status": "Computer Science & Engineering Student",
                    "gmail": "claudiuchelcea01@gmail.com", "number": "(+40) 763 665 892"}
    return render_template("Index.html", title=meta, contact=contact_data)

# Contact page
@app.route('/Contact', methods=['GET', 'POST'])
def contact():
    meta = {"title": "Contact page"}
    meta.update({"icon": "https://i.pinimg.com/originals/bb/18/bd/bb18bdbbef437b2d50518db5a8292c94.png"})
    reason = ["Other", "Project", "Job offer"]
    return render_template("Contact.html", title=meta, reasons=reason)

# Thank you page
@app.route('/ThankYou', methods=["POST"])
def thankyou():
    meta = {"title": "Thank you"}
    meta.update({"icon": "https://img.freepik.com/free-icon/present-box-with-big-bow_318-9536.jpg?size=338&ext=jpg"})
    name = request.form.get("name")
    email = request.form.get("email")
    reason = ["Other", "Project", "Job offer"]
    message = request.form.get("message")
    company = request.form.get("company")
    phone = request.form.get("phone")
    meta.update({"name": name})
    meta.update({"email": email})
    meta.update({"message": message})
    meta.update({"company": company})
    meta.update({"phone": phone})

    if not name or not email or not message or not phone or not company:
        meta["title"] = "Error"
        meta["icon"] = "https://www.freeiconspng.com/thumbs/error-icon/error-icon-3.png"
        return render_template("Error.html", title=meta, reasons=reason)

    meta["title"] = "Thank you"
    meta["icon"] = "https://img.freepik.com/free-icon/present-box-with-big-bow_318-9536.jpg?size=338&ext=jpg"
    reason = request.form.get("reason")

    # Configure an email at line 15 for the submit button to work correctly
    msg = Message('Form submission', sender=default_email, recipients=['claudiuchelcea01@gmail.com'])

    msg.body = "Name: " + name + "\n" + "Company: " + company + "\nEmail: " + email + "\nPhone number: " + \
               phone + "\n\nContact reason: " + reason + "\nMessage: " + message
    mail.send(msg)

    return render_template("ThankYou.html", title=meta, reasons=reason)

# Server
if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
