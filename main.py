from flask import Flask, render_template

#creates teh flask instance
app = Flask(__name__)

#start page of the webapplicatiop
@app.route("/")
def home():
    return render_template('index.html')

#ensures that the application keeps running
if __name__ == "__main__":
    #remove the debug=True statement before deploment
    app.run(debug=True)