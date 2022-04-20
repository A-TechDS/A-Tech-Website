from flask import Flask, flash, render_template, request, redirect, abort
from flask_mail import Mail, Message
import telegram_send

app = Flask(__name__)

# flask_mail confifg
app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'atechdesignsolutions@gmail.com'
app.config['MAIL_PASSWORD'] = 'De$ign466'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'atechdesignsolutions@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False
app.config['SECRET_KEY'] = 'secret'
mail = Mail(app)


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
    
    

@app.route('/500')
def error500():
    abort(500)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    telegram_send.send(messages=['Someone has accessed the website!'])
    return render_template('index.html')


@app.route('/OurStory')
def ourstory():
    return render_template('ourstory.html')


@app.route('/OurTeam')
def ourteam():
    return render_template('team.html')


@app.route('/Process')
def process():
    return render_template('process.html')


@app.route('/Portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/Consultation')
def consultation():

    return render_template('consultation.html')


@app.route('/Contact', methods=['GET', 'POST'])
def contact():
    company_name = request.form['company_name']
    company_usp = request.form['company_usp']
    company_email = request.form['company_email']
    name = request.form['name']

    msg_company = Message(
        'Congratulations on taking the first step!' + ' ' + name,  recipients=[company_email])
    msg_company.body = 'Thank you!' + name + ' ' + \
        'for contacting us. We will get back to you soon.' + \
        'Here are the details you provided:   ' \
        + 'Company Name:    ' + company_name + '  ' + 'Company USP:    ' + \
        company_usp + '   ' + 'Company Email:    ' + company_email
    mail.send(msg_company)
    msg_atech = Message('Contact Form Request',  recipients=[
                        'hamish@atech.industries'])
    msg_atech.body = 'New Contact Request' + 'Company Name:      ' + company_name + '   ' + \
        'Company USP:     ' + company_usp + '  ' 'Company Email:     ' + company_email
    mail.send(msg_atech)
    telegram_send.send(messages=['Someone has used the contact form!' +
                                 ' ' + company_name + ' ' + name + ' ' + company_email])
    flash('Your message has been sent!')
    return redirect('/')


@app.route('/EBook', methods=['GET', 'POST'])
def ebook():
    email = request.form['email']
    msg_client = Message('You absolute Legend!',  recipients=[email])
    msg_client.body = 'Thank you. You have just taken your first step towards becoming an absolute legend. Here is your free ebook. Enjoy!'
    #msg.attach('EBook.pdf', 'application/pdf', open('EBook.pdf', 'rb').read())
    mail.send(msg_client)
    msg_atech = Message('EBook Request',  recipients=[
                        'hamish@atech.industries'])
    msg_atech.body = 'New EBook Request' + 'Email:     ' + email
    mail.send(msg_atech)
    telegram_send.send(messages=['Someone has used the EBOOK form!' + email])
    flash('Your message has been sent!') 
    return redirect('/Consultation')


if __name__ == '__main__':
    app.run(debug=True)
