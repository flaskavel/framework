# ------------------------------------------------------------------------------
# Authorized Configuration Sections for Bootstrapping
# ------------------------------------------------------------------------------
# This tuple defines the only allowed configuration sections that can be used
# during the application's bootstrapping process.
#
# Each section represents a core component of the framework, ensuring that only
# predefined and necessary configurations are loaded at startup. This prevents
# unauthorized modifications or unintended settings from being injected.
#
# Sections:
# - app        : General application settings.
# - auth       : Authentication and authorization settings.
# - cache      : Configuration for caching mechanisms.
# - cors       : Cross-Origin Resource Sharing (CORS) policies.
# - database   : Database connection and ORM settings.
# - filesystems: File storage configurations.
# - logging    : Logging and monitoring settings.
# - mail       : Email sending and SMTP configurations.
# - queue      : Queue system settings for background tasks.
# - session    : Session management configurations.
#
# Any configuration outside these sections will be ignored or rejected.
# ------------------------------------------------------------------------------

SECTIONS = (
    'app',
    'auth',
    'cache',
    'cors',
    'database',
    'filesystems',
    'logging',
    'mail',
    'queue',
    'session'
)
