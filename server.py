from flask import Flask, request, make_response

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World"


@app.route("/dumplogs", methods=["POST"])
def dump_logs():
    # handle data
    print(request.data)
    return make_response()


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)
