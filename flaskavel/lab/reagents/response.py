from flask import jsonify, send_file, redirect
from flaskavel.lab.catalyst.http_status_code import HttpStatusCode

class Response:
    """
    Provides standardized static methods to generate common JSON responses used in web services.
    Follows a consistent format inspired by Laravel’s response methods.
    """

    @staticmethod
    def json(data:dict=None, errros:dict=None, code:int=200, message:str="Operation successful", status:str="Ok", headers:dict={}):
        """
        General method for sending a standard JSON response.

        Args:
            data (dict): The data to include in the response. Defaults to None.
            code (int): The HTTP status code. Defaults to 200.
            message (str): The message to include in the response. Defaults to "Success".
            status (str): The status text. Defaults to "Ok".
            headers (dict): Optional HTTP headers. Defaults to None.

        Returns:
            tuple: A tuple containing a JSON object, the HTTP status code, and optional headers.
        """

        response = {
            "status": status,
            "message": message,
            "data": data or {},
            "errros": errros or {}
        }

        return jsonify(response), code, headers or {}

    @staticmethod
    def success(data:dict=None, message:str="Operation successful", headers:dict=None):
        """
        Responds with a 200 OK for successful operations.
        """
        return Response.json(
            data=data,
            code=HttpStatusCode.OK.code,
            message=message,
            status=HttpStatusCode.OK.description,
            headers=headers
        )

    @staticmethod
    def created(data:dict=None, message:str="Resource created successfully", headers:dict=None):
        """
        Responds with a 201 Created when a resource is successfully created.
        """
        return Response.json(
            data=data,
            code=HttpStatusCode.CREATED.code,
            message=message,
            status=HttpStatusCode.CREATED.description,
            headers=headers
        )

    @staticmethod
    def noContent(headers:dict=None):
        """
        Responds with a 204 No Content.
        """
        return Response.json(
            data=None,
            code=HttpStatusCode.NO_CONTENT.code,
            message='',
            status=HttpStatusCode.NO_CONTENT.description,
            headers=headers
        )

    @staticmethod
    def badRequest(errros:dict=None, message:str="Bad request", headers:dict=None):
        """
        Responds with a 400 Bad Request when the request is invalid.
        """
        return Response.json(
            errros=errros,
            code=HttpStatusCode.BAD_REQUEST.code,
            message=message,
            status=HttpStatusCode.BAD_REQUEST.description,
            headers=headers
        )

    @staticmethod
    def unauthorized(message:str="Unauthorized", headers:dict=None):
        """
        Responds with a 401 Unauthorized for authentication failures.
        """
        return Response.json(
            code=HttpStatusCode.UNAUTHORIZED.code,
            message=message,
            status=HttpStatusCode.UNAUTHORIZED.description,
            headers=headers
        )

    @staticmethod
    def forbidden(message:str="Forbidden", headers:dict=None):
        """
        Responds with a 403 Forbidden when the user does not have permission.
        """
        return Response.json(
            code=HttpStatusCode.FORBIDDEN.code,
            message=message,
            status=HttpStatusCode.FORBIDDEN.description,
            headers=headers
        )

    @staticmethod
    def notFound(errros:dict=None, message:str="Resource not found", headers:dict=None):
        """
        Responds with a 404 Not Found when a resource is not found.
        """
        return Response.json(
            errros=errros,
            code=HttpStatusCode.NOT_FOUND.code,
            message=message,
            status=HttpStatusCode.NOT_FOUND.description,
            headers=headers
        )

    @staticmethod
    def unprocessableEntity(message:str="Unprocessable Entity", headers:dict=None):
        """
        Responds with a 422 Unprocessable Entity for validation errors.
        """
        return Response.json(
            code=HttpStatusCode.UNPROCESSABLE_ENTITY.code,
            message=message,
            status=HttpStatusCode.UNPROCESSABLE_ENTITY.description,
            headers=headers
        )

    @staticmethod
    def serverError(errros:dict=None, message:str="Internal server error", headers=None):
        """
        Responds with a 500 Internal Server Error for unexpected server issues.
        """
        return Response.json(
            errros=errros,
            code=HttpStatusCode.INTERNAL_SERVER_ERROR.code,
            message=message,
            status=HttpStatusCode.INTERNAL_SERVER_ERROR.description,
            headers=headers
        )

    @staticmethod
    def redirect(location):
        """
        Performs a redirect to a different location (similar to Laravel’s `redirect()`).
        """
        return redirect(location)

    @staticmethod
    def download(file_path, filename=None, mimetype=None):
        """
        Responds by sending a file to the client (similar to Laravel’s `download()`).
        """
        return send_file(file_path, as_attachment=True, download_name=filename, mimetype=mimetype)

