from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
  <head>
    <title>Demo Form</title>
    <style>
      body { font-family: sans-serif; padding: 30px; }
      form { max-width: 420px; }
      input, button { display: block; width: 100%; margin: 10px 0; padding: 10px; }
    </style>
  </head>
  <body>
    <h1>Demo Registration</h1>
    <form method="post">
      <label>First Name</label>
      <input name="first_name" id="first_name" required>

      <label>Last Name</label>
      <input name="last_name" id="last_name" required>

      <label>Email</label>
      <input type="email" name="email" id="email" required>

      <button type="submit" id="submit_button">Submit</button>
    </form>

    {% if submitted %}
      <p>Submitted successfully for {{ first_name }} {{ last_name }}.</p>
    {% endif %}
  </body>
</html>
"""

@app.get("/")
def index():
    return render_template_string(HTML, submitted=False)

@app.post("/")
def submit():
    first_name = request.form.get("first_name", "")
    last_name = request.form.get("last_name", "")
    email = request.form.get("email", "")
    return render_template_string(HTML, submitted=True, first_name=first_name, last_name=last_name, email=email)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
