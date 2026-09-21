# Welcome to Secure Code Game Season-1/Level-3!

# You know how to play by now, good luck!

import os
from flask import Flask, request

### Unrelated to the exercise -- Starts here -- Please ignore
app = Flask(__name__)
@app.route("/")
def source():
    TaxPayer('foo', 'bar').get_tax_form_attachment(request.args["input"])
    TaxPayer('foo', 'bar').get_prof_picture(request.args["input"])
### Unrelated to the exercise -- Ends here -- Please ignore

class TaxPayer:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.prof_picture = None
        self.tax_form_attachment = None

    def get_prof_picture(self, path=None):
        if not path:
            return None
        base = os.path.realpath(os.path.dirname(__file__))
        safe_path = os.path.realpath(os.path.join(base, path))
        # Include the separator so sibling names cannot match this directory.
        if not safe_path.startswith(base + os.sep):
            return None
        with open(safe_path, 'rb') as pic:
            picture = bytearray(pic.read())
        return safe_path

    def get_tax_form_attachment(self, path=None):
        if not path:
            raise ValueError("Error: Tax form is required for all users")
        base = os.path.realpath(os.path.dirname(__file__))
        safe_path = os.path.realpath(os.path.join(base, path))
        # Include the separator so sibling names cannot match this directory.
        if not safe_path.startswith(base + os.sep):
            return None
        with open(safe_path, 'rb') as form:
            tax_data = bytearray(form.read())
        return safe_path
