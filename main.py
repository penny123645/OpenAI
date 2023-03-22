# main.py

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Flask!"

@app.route("/apple")
def apple():
    return "I am apple!"

@app.route('/add/num1=<num1>&num2=<num2>', methods=['GET'])
def add(num1,num2):
    print(num1 + num2)
    return str(int(num1) + int(num2))
    
if __name__ == "__main__":
    app.run()