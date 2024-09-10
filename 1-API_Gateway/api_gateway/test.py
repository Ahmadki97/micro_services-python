from flask import Flask, request

app = Flask(__name__)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_data()
    print(data)
    return("Hello from Signup")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='4000', debug=True)