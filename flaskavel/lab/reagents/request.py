from flask import request
from typing import Any, List, Dict

class Request:
    """A class to handle HTTP request data in a Flaskavel application."""

    @classmethod
    @property
    def path(cls) -> str:
        """Returns the current path of the URL."""
        return request.path if request.path else None

    @classmethod
    @property
    def fullUrl(cls) -> str:
        """Returns the complete URL including query parameters."""
        return request.url

    @classmethod
    @property
    def fullUrlWithoutQuery(cls) -> str:
        """Returns the complete URL without query parameters."""
        return request.base_url

    @classmethod
    @property
    def fullUrlWithQuery(cls) -> str:
        """Returns the complete URL along with all query parameters."""
        return request.url

    @classmethod
    @property
    def host(cls) -> str:
        """Returns the host."""
        return request.host

    @classmethod
    @property
    def httpHost(cls) -> str:
        """Returns the complete HTTP host, including the port."""
        return request.host_url

    @classmethod
    @property
    def scheme(cls) -> str:
        """Returns the scheme of the URL (http or https)."""
        return request.scheme

    @classmethod
    @property
    def schemeAndHttpHost(cls) -> str:
        """Returns the scheme and the complete host."""
        return f"{request.scheme}://{request.host}"

    @classmethod
    def isMethod(cls, method: str) -> bool:
        """Checks if the HTTP method matches the one provided as an argument."""
        return request.method.upper() == method.upper()

    @classmethod
    def header(cls, header: str) -> Any:
        """Retrieves a value from the request header."""
        return request.headers.get(header, None)

    @classmethod
    def hasHeader(cls, header: str) -> bool:
        """Checks if a specific header is present in the request."""
        return header in request.headers

    @classmethod
    @property
    def ip(cls) -> str:
        """Returns the IP address of the client making the request."""
        return request.remote_addr if request.remote_addr else None

    @classmethod
    @property
    def bearerToken(cls) -> str:
        """Returns the Bearer token from the Authorization header if present."""
        auth_header = request.headers.get('Authorization', None)
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None

    @classmethod
    @property
    def ips(cls) -> List[str]:
        """Returns a list of all IPs (client and proxies) that have sent the request."""
        if 'X-Forwarded-For' in request.headers:
            return [ip.strip() for ip in request.headers['X-Forwarded-For'].split(',')]
        return [request.remote_addr]

    @classmethod
    @property
    def getAcceptableContentTypes(cls) -> List[str]:
        """Returns a list of acceptable content types specified in the `Accept` header."""
        return list(request.accept_mimetypes.values())

    @classmethod
    def accepts(cls, content_types: List[str]) -> bool:
        """Checks if any of the content types in the list are accepted by the client."""
        return any(content_type in request.accept_mimetypes for content_type in content_types)

    @classmethod
    def all(cls) -> Dict[str, Any]:
        """Returns all the data sent, both in the query and in the body (POST)."""
        data = request.get_json(silent=True) or {}
        if request.form:
            data.update(request.form.to_dict())
        data.update(request.args.to_dict())
        return data

    @classmethod
    def input(cls, key: str) -> Any:
        """Returns all the data sent, using `.to_dict()` to ensure compatibility."""
        data = cls.all()
        if key in data:
            return data.get(key)
        raise ValueError(f"The key '{key}' is not present in the request.")

    @classmethod
    def query(cls, key: str = None, default: Any = None) -> Any:
        """Gets a specific value from the query string or all parameters if none is specified."""
        if key:
            return request.args.get(key, default)
        return request.args.to_dict()

    @classmethod
    def only(cls, keys: List[str]) -> Dict[str, Any]:
        """Returns only the specified fields from the body or query string."""
        data = cls.all()
        return {key: data[key] for key in keys if key in data}

    @classmethod
    def exclude(cls, keys: List[str]) -> Dict[str, Any]:
        """Returns all fields except the specified ones."""
        data = cls.all()
        return {key: value for key, value in data.items() if key not in keys}

    @classmethod
    def has(cls, key: str) -> bool:
        """Checks if a field is present in the query string or in the request body."""
        return key in cls.all()

    @classmethod
    def hasAny(cls, keys: List[str]) -> bool:
        """Checks if at least one of the specified fields is present in the request."""
        return any(key in cls.all() for key in keys)

    @classmethod
    def file(cls, key: str) -> Any:
        """Returns an uploaded file if it exists."""
        return request.files.get(key)

    @classmethod
    def hasFile(cls, key: str) -> bool:
        """Checks if a file has been uploaded with the specified name."""
        return key in request.files

    @classmethod
    def validate(cls, rules = None, messages = None, form_request = None) -> bool:
        """
        Validates the request data against provided rules and messages.

        Args:
            rules (Optional[Dict[str, Any]]): Validation rules to apply.
            messages (Optional[Dict[str, str]]): Custom error messages.
            form_request (Optional[FormRequest]): An optional FormRequest instance for validation.

        Returns:
            bool: True if validation is successful.
        """

        # Import FormRequest only when needed for easier loading
        from flaskavel.lab.alchemist.http.base_form_request import FormRequest

        # Check if a FormRequest instance is provided
        if form_request is not None:
            form_request.validated()
            return True

        # If no FormRequest is provided, create a standard request class
        class StdRequest(FormRequest):
            def __init__(self):
                super().__init__(data=cls.all())

            def rules(self) -> Dict[str, Any]:
                return rules or {}

            def messages(self) -> Dict[str, str]:
                return messages or {}

        # Validate using the standard request
        StdRequest().validated()
        return True
