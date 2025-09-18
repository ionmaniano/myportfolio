from flask import *
import pymysql



# Initialize Flask app
app = Flask(__name__)


connection=pymysql.connect(host='localhost',user='root',password='',database='myportfolio') #creating a connection to our database using function connect
cursor=connection.cursor()
app.secret_key="bazenga" #We are cerating secret keys to secure our sessions/make it unique

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# about Route
@app.route('/about')
def about():
    return render_template('about.html')

# about Route
@app.route('/education')
def education():
    return render_template('education.html')

# about Route
@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/contacts', methods=['POST', 'GET'])
def contacts():
        if request.method == 'POST':
            Name = request.form['Name']
            Email = request.form['Email']
            Subject = request.form['Subject']
            Message = request.form['Message']

            
            cursor = connection.cursor()

            sql = "INSERT INTO contact_info (Name,Email,Subject, Message) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (Name,Email,Subject, Message))

            connection.commit()
            cursor.close()
            connection.close()
        
        return render_template('contacts.html', message='Sent successfuly')
# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, port=5050)
