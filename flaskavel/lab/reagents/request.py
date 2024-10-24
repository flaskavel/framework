from flask import request
from typing import Any, List, Dict

class Request:

    @classmethod
    @property
    def path(cls) -> str:
        """Devuelve el path actual de la URL."""
        return request.path if request.path else None

    @classmethod
    @property
    def fullUrl(cls) -> str:
        """Devuelve la URL completa incluyendo los parámetros de query."""
        return request.url

    @classmethod
    @property
    def fullUrlWithoutQuery(cls) -> str:
        """Devuelve la URL completa pero sin los parámetros de query."""
        return request.base_url

    @classmethod
    @property
    def fullUrlWithQuery(cls) -> str:
        """Devuelve la URL completa junto con todos los parámetros de query."""
        return request.url

    @classmethod
    @property
    def host(cls) -> str:
        """Devuelve el host."""
        return request.host

    @classmethod
    @property
    def httpHost(cls) -> str:
        """Devuelve el HTTP host completo, incluyendo el puerto."""
        return request.host_url

    @classmethod
    @property
    def scheme(cls) -> str:
        """Devuelve el esquema de la URL (http, https)."""
        return request.scheme

    @classmethod
    @property
    def schemeAndHttpHost(cls) -> str:
        """Devuelve el esquema y el host completo."""
        return f"{request.scheme}://{request.host}"

    @classmethod
    def isMethod(cls, method: str) -> bool:
        """Verifica si el método HTTP coincide con el pasado como argumento."""
        return request.method.upper() == method.upper()

    @classmethod
    def header(cls, header: str) -> Any:
        """Obtiene un valor del encabezado."""
        return request.headers.get(header, None)

    @classmethod
    def hasHeader(cls, header: str) -> bool:
        """Verifica si un encabezado específico está presente."""
        return header in request.headers

    @classmethod
    @property
    def ip(cls) -> str:
        """Devuelve la IP del cliente que realiza la solicitud."""
        return request.remote_addr if request.remote_addr else None

    @classmethod
    @property
    def bearerToken(cls) -> str:
        """Devuelve el token Bearer del encabezado de Autorización si está presente."""
        auth_header = request.headers.get('Authorization', None)
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None

    @classmethod
    @property
    def ips(cls) -> List[str]:
        """Devuelve una lista de todas las IPs (cliente y proxies) que han enviado la solicitud."""
        if 'X-Forwarded-For' in request.headers:
            return [ip.strip() for ip in request.headers['X-Forwarded-For'].split(',')]
        return [request.remote_addr]

    @classmethod
    @property
    def getAcceptableContentTypes(cls) -> List[str]:
        """Devuelve una lista de los tipos de contenido aceptables especificados en el encabezado `Accept`."""
        return list(request.accept_mimetypes.values())

    @classmethod
    def accepts(cls, content_types: List[str]) -> bool:
        """Verifica si alguno de los tipos de contenido en la lista es aceptado por el cliente."""
        return any(content_type in request.accept_mimetypes for content_type in content_types)

    @classmethod
    def all(cls) -> Dict[str, Any]:
        """Devuelve todos los datos enviados, tanto en la query como en el cuerpo (POST)."""
        return request.values.to_dict()

    @classmethod
    def collect(cls) -> Dict[str, Any]:
        """Devuelve todos los datos enviados, utilizando `.to_dict()` para asegurar compatibilidad."""
        return request.values.to_dict()

    @classmethod
    def query(cls, key: str = None, default: Any = None) -> Any:
        """Obtiene un valor específico de la query string o todos los parámetros si no se especifica."""
        if key:
            return request.args.get(key, default)
        return request.args.to_dict()

    @classmethod
    def only(cls, keys: List[str]) -> Dict[str, Any]:
        """Devuelve solo los campos especificados en el cuerpo o la query string."""
        return {key: request.values.get(key) for key in keys if key in request.values}

    @classmethod
    def exclude(cls, keys: List[str]) -> Dict[str, Any]:
        """Devuelve todos los campos excepto los especificados."""
        return {key: request.values.get(key) for key in request.values if key not in keys}

    @classmethod
    def has(cls, key: str) -> bool:
        """Verifica si un campo está presente en la query string o en el cuerpo de la solicitud."""
        return key in request.values

    @classmethod
    def hasAny(cls, keys: List[str]) -> bool:
        """Verifica si al menos uno de los campos especificados está presente en la solicitud."""
        return any(key in request.values for key in keys)

    @classmethod
    def file(cls, key: str) -> Any:
        """Devuelve un archivo subido, si existe."""
        return request.files.get(key)

    @classmethod
    def hasFile(cls, key: str) -> bool:
        """Verifica si se ha subido un archivo con el nombre especificado."""
        return key in request.files
