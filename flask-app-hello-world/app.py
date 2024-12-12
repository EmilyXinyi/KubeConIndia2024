from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def hello_world():
  return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
</head>
<body>
    <h1>Hello KubeCon!</h1>
</body>
</html>
''')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)