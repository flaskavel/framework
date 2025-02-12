from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict

@dataclass
class Data:
    """
    Interface that defines the structure for configuring Cross-Origin Resource Sharing (CORS)
    for Starlette's CORSMiddleware.

    Attributes
    ----------
    allowed_methods : List[str]
        A list of HTTP methods (e.g., "GET", "POST", "PUT", etc.) that are allowed for cross-origin requests.

    allowed_origins : Union[str, List[str]]
        A single origin or a list of origins that are allowed to access the resources.
        Example: "https://example.com" or ["https://example.com", "https://another-origin.com"].

    allowed_headers : List[str]
        A list of headers that can be included in the requests from the allowed origins.
        Example: ["Content-Type", "X-Custom-Header"].

    exposed_headers : List[str]
        A list of headers that the browser can access from the response.
        Example: ["X-Exposed-Header"].

    max_age : Optional[int]
        The maximum amount of time (in seconds) that the results of a preflight request can be cached by the browser.

    custom : Dict[str, any]
        A dictionary for any custom properties or additional configurations related to CORS.
        This field is initialized with an empty dictionary by default.

    Notes
    -----
    - `allowed_methods`, `allowed_headers`, and `exposed_headers` should always be lists of strings.
    - `allowed_origins` can either be a single string or a list of strings.
    - `max_age` should be an integer representing the duration in seconds.
    - The `custom` attribute is for additional configurations or custom properties.
    """

    # List of allowed HTTP methods
    allowed_methods: List[str]

    # Single origin or list of origins allowed
    allowed_origins: Union[str, List[str]]

    # List of allowed headers
    allowed_headers: List[str]

    # List of headers that are accessible by the browser
    exposed_headers: List[str]

    # Time in seconds that the results of preflight requests can be cached
    max_age: Optional[int]

    # Custom properties or configurations for additional flexibility
    custom: Dict[str, any] = field(default_factory=dict)
