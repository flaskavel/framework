from flask import request

class Request:

    def __init__(self, request):
        self._request = request

    # Like $request->input() from Laravel
    def input(self, key=None, default=None):
        """
        Get input from form data, JSON body, or query parameters (GET).
        """
        if key:
            return self._request.form.get(key) or self._request.args.get(key) or self._request.json.get(key, default)
        else:
            # If no key is provided, return all data (POST, GET, JSON)
            combined = {}
            combined.update(self._request.form.to_dict())
            combined.update(self._request.args.to_dict())
            if self._request.json:
                combined.update(self._request.json)
            return combined

    # Like $request->query() from Laravel
    def query(self, key=None, default=None):
        """
        Get query parameter value.
        """
        if key:
            return self._request.args.get(key, default)
        return self._request.args

    # Like $request->json() from Laravel
    def json(self, key=None, default=None):
        """
        Get data from the JSON body.
        """
        if self._request.is_json:
            if key:
                return self._request.json.get(key, default)
            return self._request.json
        return {}

    # Like $request->file() from Laravel
    def file(self, key=None):
        """
        Get a file from the uploaded files.
        """
        if key:
            return self._request.files.get(key)
        return self._request.files

    # Like $request->header() from Laravel
    def header(self, key=None, default=None):
        """
        Get a specific header value.
        """
        if key:
            return self._request.headers.get(key, default)
        return self._request.headers

    # Like $request->isMethod('post') from Laravel
    def is_method(self, method):
        """
        Check if the current request is of a specific method.
        """
        return self._request.method.upper() == method.upper()

    # Like $request->all() from Laravel
    def all(self):
        """
        Get all input from form, query parameters, and JSON body.
        """
        return self.input()

    # Like $request->has() from Laravel
    def has(self, key):
        """
        Check if the request has a specific input.
        """
        return key in self._request.form or key in self._request.args or (self._request.json and key in self._request.json)

    # Like $request->except() from Laravel
    def except_(self, *keys):
        """
        Return all inputs except the given keys.
        """
        data = self.all()
        for key in keys:
            if key in data:
                del data[key]
        return data

    # Like $request->only() from Laravel
    def only(self, *keys):
        """
        Return only the specified keys from the request.
        """
        data = self.all()
        return {key: data[key] for key in keys if key in data}
