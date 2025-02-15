from dataclasses import dataclass
from typing import Optional

@dataclass
class Local:
    """
    Represents a local filesystem configuration.

    Attributes
    ----------
    path : str
        The absolute or relative path where local files are stored.
    """
    path: str


@dataclass
class Public:
    """
    Represents a public filesystem configuration.

    Attributes
    ----------
    path : str
        The public-facing path where files are stored.
    slug : str
        A unique identifier for the public storage location.
    """
    path: str
    slug: str


@dataclass
class AWSS3:
    """
    Represents an AWS S3 storage configuration.

    Attributes
    ----------
    driver : str
        The storage driver (default: 's3').
    key : str
        AWS access key ID.
    secret : str
        AWS secret access key.
    region : str
        AWS region where the bucket is located.
    bucket : str
        The S3 bucket name.
    url : Optional[str], default=None
        The URL endpoint for accessing the S3 bucket.
    endpoint : Optional[str], default=None
        The AWS S3 endpoint URL.
    use_path_style_endpoint : bool, default=False
        Whether to use a path-style endpoint.
    throw : bool, default=False
        Whether to raise an exception on errors.
    """
    key: str = ""
    secret: str = ""
    region: str = "us-east-1"
    bucket: str = ""
    url: Optional[str] = None
    endpoint: Optional[str] = None
    use_path_style_endpoint: bool = False
    throw: bool = False


@dataclass
class Disks:
    """
    Represents the available storage disks.

    Attributes
    ----------
    local : Local
        Configuration for local storage.
    public : Public
        Configuration for public storage.
    s3 : AWSS3
        Configuration for AWS S3 storage.
    """
    local: Local
    public: Public
    s3: AWSS3


@dataclass
class Filesystems:
    """
    Represents the filesystem configuration, supporting multiple storage disks.

    Attributes
    ----------
    default : str
        The default storage disk to use.
    disks : Disks
        A collection of configured storage disks.
    """

    default: str
    disks: Disks
