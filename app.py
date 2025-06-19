from flask import *
import pymysql



# Initialize Flask app
app = Flask(__name__)


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

@app.route('/contacts.html')
def contacts():
    
    return render_template('contacts.html')

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True, port=5050)
