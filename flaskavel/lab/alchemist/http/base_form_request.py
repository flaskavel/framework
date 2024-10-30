import re
import uuid
import socket
from datetime import datetime
from flaskavel.lab.catalyst.exceptions import *

class FormRequest:

    def __init__(self, data: dict = None):
        # Store the Request data in this variable.
        self.data = data
        # Store the first generated error in this variable.
        self.first_error = None
        # Collect generated errors in this dictionary.
        self.errors = {}

    def authorize(self):
        # Can be overridden in subclasses to allow or deny access.
        return True

    def rules(self):
        # Define validation rules for fields. Can be overridden in subclasses.
        return {}

    def messages(self):
        # Define custom error messages. Can be overridden in subclasses.
        return {}

    def validate(self):
        """
        Validate the request data against defined rules and messages.

        Raises:
            Exception: If authorization fails or validation errors are found.

        Returns:
            bool: True if all validation passes and authorization is granted.
        """

        # Raise 403 Exception if authorization fails.
        if not self.authorize():
            raise AuthorizeFlaskavelException("Unauthorized request")

        # Capture validation rules.
        rules = self.rules()

        # Ensure there are rules to iterate over.
        if len(rules) > 0:

            # Iterate over each field and apply rules.
            for field, rules in self.rules().items():
                self.apply_rules_to_field(field, rules)

            # Raise 422 Exception if any validation errors are present.
            if self.errors:
                raise ValidateFlaskavelException(self.get_errors())

        return True

    def apply_rules_to_field(self, field, rules):
        """
        Apply a set of rules to a specific field in the request data.

        Args:
            field (str): The field name in the data.
            rules (str): The validation rules as a pipe-separated string.
        """

        # Split the rules by pipe character.
        validations = rules.split('|')

        # Apply rules for nested list notation.
        if '.*.' in field:
            self.apply_array_rules(field, validations)

        # Apply validation for simple fields.
        else:
            for validation in validations:
                self.apply_rule(field, validation)

    def dot_notation_access(self, field: str):
        """
        Access nested data in the request using dot notation.

        Args:
            field (str): The field name with dot notation to access nested values.

        Returns:
            The value found or None if not accessible.
        """

        # Ensure field is a valid key.
        if not field:
            raise ValueError("Field keys cannot be null in validation rules.")

        # Split the field by dots.
        field_indexes = field.split('.')

        # Initialize the first index.
        index = self.data.get(field_indexes[0])

        # Traverse further if additional indexes exist.
        if len(field_indexes) > 1:
            try:
                # Dynamically update index as it iterates over keys.
                for key in field_indexes[1:]:
                    if str(key).isdigit():
                        index = index[int(key)]
                    else:
                        index = index.get(key) if isinstance(index, dict) else None
                    if index is None:
                        break
            except Exception:
                return None

        return index

    def accepted(self, value):
        """
        Ensures the field is accepted. The field must be one of the following values:
        "yes", "on", 1, "1", true, or "true".
        This validation is typically used for fields that require explicit user acceptance,
        such as "Terms of Service".

        Args:
            value (any): The value to validate.

        Returns:
            bool: True if the value is one of the accepted values, False otherwise.
        """
        accepted_values = {"yes", "on", 1, "1", True, "True", "true"}
        return value in accepted_values

    def active_url(self, value):
        """
        Ensures that the field contains a valid URL with an existing DNS A or AAAA record.
        This validation checks if the hostname in the provided URL can be resolved to an IP address,
        verifying its active status.

        Args:
            value (str): The URL string to validate.

        Returns:
            bool: True if the URL has a valid DNS A or AAAA record; False otherwise.
        """
        if not 'http' in value:
            return False

        import socket
        from urllib.parse import urlparse

        try:
            # Parse URL to get hostname
            hostname = urlparse(value).hostname
            if hostname is None:
                return False

            # Check for DNS A or AAAA records
            socket.gethostbyname(hostname)
            return True

        except (socket.gaierror, ValueError):
            return False

    def after(self, value, date:str):
        """
        Ensures that the field contains a date after a specified date.
        Converts both the field date and comparison date to DateTime instances for accurate comparison.

        Args:
            value (str): The date to validate, as a string in a standard date format (e.g., "YYYY-MM-DD").
            date (str): The date to compare against, also as a string in a standard date format.

        Returns:
            bool: True if the 'value' date is after the specified 'date'; False otherwise.
        """
        try:
            value_date = datetime.strptime(value, "%Y-%m-%d")
            comparison_date = datetime.strptime(date, "%Y-%m-%d")
            return value_date > comparison_date
        except ValueError:
            return False

    def after_or_equal(self, value, date):
        """
        Ensures that the field contains a date that is equal to or after a specified date.
        Converts both the field date and comparison date to DateTime instances for accurate comparison.

        Args:
            value (str): The date to validate, as a string in a standard date format (e.g., "YYYY-MM-DD").
            date (str): The date to compare against, also as a string in a standard date format.

        Returns:
            bool: True if the 'value' date is equal to or after the specified 'date'; False otherwise.
        """
        try:
            value_date = datetime.strptime(value, "%Y-%m-%d")
            comparison_date = datetime.strptime(date, "%Y-%m-%d")
            return value_date >= comparison_date
        except ValueError:
            return False

    def before(self, value, date):
        """
        Validates that the date in `value` occurs before the specified `date`.

        Args:
            value (str): The date string to validate in 'YYYY-MM-DD' format.
            date (str): The comparison date string in 'YYYY-MM-DD' format.

        Returns:
            bool: True if `value` is before `date`, otherwise False.

        Raises:
            ValueError: If the date format in `value` or `date` is invalid.
        """
        try:
            value_date = datetime.strptime(value, '%Y-%m-%d')
            compare_date = datetime.strptime(date, '%Y-%m-%d')
            return value_date < compare_date
        except ValueError:
            return False

    def before_or_equal(self, value, date):
        """
        Validates that the date in `value` occurs on or before the specified `date`.

        Args:
            value (str): The date string to validate in 'YYYY-MM-DD' format.
            date (str): The comparison date string in 'YYYY-MM-DD' format.

        Returns:
            bool: True if `value` is on or before `date`, otherwise False.

        Raises:
            ValueError: If the date format in `value` or `date` is invalid.
        """
        try:
            value_date = datetime.strptime(value, '%Y-%m-%d')
            compare_date = datetime.strptime(date, '%Y-%m-%d')
            return value_date <= compare_date
        except ValueError:
            return False

    def between(self, value, min_value, max_value):
        """
        Validates that `value` is between the specified `min_value` and `max_value`.

        Args:
            value (int, float): The value to validate.
            min_value (int, float): The minimum permissible value.
            max_value (int, float): The maximum permissible value.

        Returns:
            bool: True if `value` is between `min_value` and `max_value` (inclusive).

        Raises:
            ValueError: If `min_value` or `max_value` are not valid numeric types.
        """
        if not isinstance(min_value, (int, float)) or not isinstance(max_value, (int, float)):
            raise ValueError("`min_value` and `max_value` must be numeric for 'between' validation.")
        if isinstance(value, (int, float)):
            return min_value <= value <= max_value
        return False

    def boolean(self, value):
        """
        Validates that the `value` can be cast as a boolean.

        Accepted inputs are True, False, 1, 0, "1", and "0".

        Args:
            value: The value to validate as boolean-compatible.

        Returns:
            bool: True if `value` can be cast to a boolean, otherwise False.
        """
        return value in [True, False, "True", "False", "true", "false", 1, 0, "1", "0"]

    def contains(self, value, *required_values):
        """
        Validates that `value` is an array containing all specified `required_values`.

        Args:
            value (list): The array or list to be validated.
            *required_values: Values that must be present in `value`.

        Returns:
            bool: True if `value` contains all items in `required_values`, otherwise False.
        """
        # Ensure the value is a list
        if not isinstance(value, list):
            return False

        # Check that all required values are in the list
        return all(item in value for item in required_values)

    def date(self, value):
        """
        Validates that `value` is a valid, non-relative date.

        Args:
            value (str): The date string to be validated.

        Returns:
            bool: True if `value` is a valid date format, otherwise False.
        """
        try:
            # Attempt to parse the date string using a common format
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def date_equals(self, value, target_date):
        """
        Validates that `value` is a date equal to the `target_date`.

        Args:
            value (str): The date string to be validated.
            target_date (str): The target date to compare against, in 'YYYY-MM-DD' format.

        Returns:
            bool: True if `value` equals `target_date`, otherwise False.
        """
        try:
            # Parse both dates and check for equality
            value_date = datetime.strptime(value, '%Y-%m-%d')
            target_date_obj = datetime.strptime(target_date, '%Y-%m-%d')
            return value_date == target_date_obj
        except ValueError:
            return False

    def decimal(self, value, min_decimals, max_decimals=None):
        """
        Validates that `value` is numeric and has a specified number of decimal places.

        Args:
            value (str or float): The value to be validated.
            min_decimals (int): The minimum number of decimal places required.
            max_decimals (int, optional): The maximum number of decimal places allowed.
                                           If None, only min_decimals is enforced.

        Returns:
            bool: True if `value` is a valid decimal with the specified decimal places, otherwise False.
        """
        # Check if the value is numeric
        if isinstance(value, (int, float)):
            # Convert to string for decimal place validation
            value_str = str(value)
        elif isinstance(value, str):
            # Check if it's a valid float string
            if not re.match(r'^-?\d+(\.\d+)?$', value):
                return False
            value_str = value
        else:
            return False

        # Split the number into whole and decimal parts
        if '.' in value_str:
            whole_part, decimal_part = value_str.split('.')
        else:
            whole_part, decimal_part = value_str, ''

        # Count the length of the decimal part
        decimal_length = len(decimal_part)

        # Validate against min and max decimal places
        if max_decimals is not None:
            return min_decimals <= decimal_length <= max_decimals
        return decimal_length == min_decimals

    def declined(self, value):
        """
        Validates that the `value` is equivalent to a declined response.

        Args:
            value (str, int, bool): The value to be validated.

        Returns:
            bool: True if `value` is equivalent to a declined response, otherwise False.
        """
        # Define accepted values for decline
        declined_values = {"no", "off", 0, "0", False, "False", "false"}

        # Return True if the value is in the accepted declined values
        return value in declined_values

    def different(self, value, field_value):
        """
        Validates that the `value` is different from the specified `field_value`.

        Args:
            value (any): The value to be validated.
            field_value (any): The value to compare against.

        Returns:
            bool: True if `value` is different from `field_value`, otherwise False.
        """
        return value != field_value

    def digits(self, value, length):
        """
        Validates that the integer `value` has an exact length of `length`.

        Args:
            value (int): The integer to be validated.
            length (int): The exact length the integer should have.

        Returns:
            bool: True if `value` has the exact length, otherwise False.
        """
        if isinstance(value, int):
            return len(str(abs(value))) == length  # Use absolute value to ignore negative sign
        return False

    def digits_between(self, value, min_length, max_length):
        """
        Validates that the integer `value` has a length between `min_length` and `max_length`.

        Args:
            value (int): The integer to be validated.
            min_length (int): The minimum length.
            max_length (int): The maximum length.

        Returns:
            bool: True if `value` has a length between min_length and max_length, otherwise False.
        """
        if isinstance(value, int):
            length = len(str(abs(value)))  # Use absolute value to ignore negative sign
            return min_length <= length <= max_length
        return False

    def email(self, value):
        """
        Validates that the input `value` is a valid email address.

        Args:
            value (str): The email address to validate.

        Returns:
            bool: True if `value` is a valid email address, otherwise False.
        """
        # Define a regular expression pattern for validating email addresses
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Use re.match to check if the value matches the email pattern
        return bool(re.match(email_pattern, value))

    def integer(self, value):
        # Ensures the value is a valid integer.
        return isinstance(value, int)

    def ip(self, value):
        """
        Validates that the value is a valid IP address (either IPv4 or IPv6).

        Args:
            value (str): The value to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            # Check for IPv4
            socket.inet_pton(socket.AF_INET, value)
            return True
        except socket.error:
            try:
                # Check for IPv6
                socket.inet_pton(socket.AF_INET6, value)
                return True
            except socket.error:
                return False

    def ipv4(self, value):
        """
        Validates that the value is a valid IPv4 address.

        Args:
            value (str): The value to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            socket.inet_pton(socket.AF_INET, value)
            return True
        except socket.error:
            return False

    def ipv6(self, value):
        """
        Validates that the value is a valid IPv6 address.

        Args:
            value (str): The value to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        try:
            socket.inet_pton(socket.AF_INET6, value)
            return True
        except socket.error:
            return False

    def lowercase(self, value):
        """
        Validates that the field value is in lowercase.

        Args:
            value (str): The value to validate.

        Returns:
            bool: True if the value is lowercase, False otherwise.
        """
        if not isinstance(value, str):
            return False

        return value.islower()

    def mac_address(self, value):
        """
        Validates that the field value is a valid MAC address.

        Args:
            value (str): The value to validate.

        Returns:
            bool: True if the value is a valid MAC address, False otherwise.
        """
        # Define the regular expression for a valid MAC address
        mac_regex = r"^([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})$"

        if not isinstance(value, str):
            return False

        # Use regex to check if the value matches the MAC address format
        return bool(re.match(mac_regex, value))

    def max(self, value, max_val):
        """
        Ensures the value does not exceed the specified maximum.

        Args:
            value: The value to validate.
            max_val (int/float): The maximum allowed value.

        Returns:
            bool: True if value is within the max_val, False otherwise.
        """
        if not isinstance(max_val, (int, float)):
            raise ValueError("The max value for validation should be an int or float.")

        if not str(value).isnumeric() or not isinstance(value, (int, float)):
            return False

    def max_digits(self, value, max_value):
        """
        Validates that the integer has a maximum length of the specified value.

        Args:
            value (int): The integer to validate.
            max_value (int): The maximum length allowed.

        Returns:
            bool: True if the integer has a length less than or equal to max_value, False otherwise.
        """
        if not isinstance(value, int):
            return False

        # Convert the integer to string to check its length
        value_length = len(str(abs(value)))  # Use abs to handle negative numbers
        return value_length <= max_value

    def min(self, value, min_val):
        """
        Ensures the value meets the specified minimum.

        Args:
            value: The value to validate.
            min_val (int/float): The minimum allowed value.

        Returns:
            bool: True if value meets or exceeds min_val, False otherwise.
        """
        if not isinstance(min_val, (int, float)):
            raise ValueError("The min value for validation should be an int or float.")

        if not str(value).isnumeric() or not isinstance(value, (int, float)):
            return False

    def min_digits(self, value, min_value):
        """
        Validates that the integer has a minimum length of the specified value.

        Args:
            value (int): The integer to validate.
            min_value (int): The minimum length required.

        Returns:
            bool: True if the integer has a length greater than or equal to min_value, False otherwise.
        """
        if not isinstance(value, int):
            return False  # The value is not an integer, return False

        # Convert the integer to string to check its length
        value_length = len(str(abs(value)))  # Use abs to handle negative numbers
        return value_length >= min_value

    def multiple_of(self, value, multiple):
        """
        Validates that the field under validation is a multiple of the specified value.

        Args:
            value (int or float): The number to validate.
            multiple (int or float): The value that must be a multiple of.

        Returns:
            bool: True if value is a multiple of multiple, False otherwise.
        """
        if not isinstance(value, (int, float)) or not isinstance(multiple, (int, float)):
            return False  # Ensure both value and multiple are numeric

        if multiple == 0:
            return False  # Cannot be a multiple of zero

        return value % multiple == 0

    def nullable(self, value):
        """
        Validates that the field under validation may be null.

        Args:
            value: The value to validate.

        Returns:
            bool: True if the value is None or any non-null value, False otherwise.
        """
        return value is None or value is not None

    def numeric(self, value):
        """
        Validates that the field under validation must be numeric.

        Args:
            value: The value to validate.

        Returns:
            bool: True if the value is numeric, False otherwise.
        """
        return isinstance(value, (int, float)) or (isinstance(value, str) and value.isnumeric())

    def regex(self, value, pattern):
        """
        Validates that the field under validation must match the given regular expression.

        Args:
            value: The value to validate.
            pattern: The regular expression pattern to match against.

        Returns:
            bool: True if the value matches the pattern, False otherwise.
        """
        if isinstance(value, str):
            return bool(re.match(pattern, value))
        return False

    def required(self, value):
        """
        Validates that the field under validation must be present in the input data and not empty.

        Args:
            value: The value to validate.

        Returns:
            bool: True if the value is present and not empty, False otherwise.
        """
        # Check if value is None (null)
        if value is None:
            return False
        # Check if value is an empty string
        if isinstance(value, str) and value.strip() == '':
            return False
        # Check if value is an empty list or tuple
        if isinstance(value, (list, tuple)) and len(value) == 0:
            return False
        # Check if value is an empty dictionary
        if isinstance(value, dict) and len(value) == 0:
            return False

        # If none of the conditions are met, the value is considered valid
        return True

    def size(self, value, size):
        """
        Validates that the field under validation must have a size matching the given value.

        Args:
            value: The value to validate (string, integer, list, or file).
            size: The required size.

        Returns:
            bool: True if the size matches, False otherwise.
        """
        # Validate if value is a string
        if isinstance(value, str):
            return len(value) == size

        # Validate if value is a number (int or float)
        if isinstance(value, (int, float)):
            return value == size

        # Validate if value is a list
        if isinstance(value, list):
            return len(value) == size

        # Validate if value is a dictionary representing a file
        if isinstance(value, dict) and 'size' in value:
            return value['size'] == size

        # If value does not match any of the expected types, return False
        return False

    def string(self, value):
        """
        Validates that the field under validation must be a string.

        Returns:
            bool: True if the value is a string or None if nullable is True,
                  False otherwise.
        """
        return isinstance(value, str)

    def url(self, value, protocols=None):
        """
        Validates that the field under validation must be a valid URL.
        Optionally, specify the allowed protocols.

        Args:
            value: The value to validate.
            protocols: A list of allowed URL protocols (default: None).

        Returns:
            bool: True if the value is a valid URL, False otherwise.
        """
        # Regex pattern for validating URLs
        url_pattern = re.compile(
            r'^(?:http|https)://'  # Match 'http://' or 'https://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,})|'  # Domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # OR IPv4...
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # OR IPv6...
            r'(?::\d+)?'  # Optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if protocols:
            # Create a regex pattern for specified protocols
            protocols_pattern = '|'.join(protocols)
            url_pattern = re.compile(
                rf'^(?:{protocols_pattern})://'  # Match specified protocols
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,})|'
                r'localhost|'
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
                r'\[?[A-F0-9]*:[A-F0-9:]+\]?)(?::\d+)?'
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return bool(url_pattern.match(value))

    def ulid(self, value):
        """
        Validates that the field under validation must be a valid ULID.

        Args:
            value: The value to validate.

        Returns:
            bool: True if the value is a valid ULID, False otherwise.
        """
        ulid_pattern = re.compile(r'^[0-9A-HJKMNP-TV-Z]{26}$')
        return bool(ulid_pattern.match(value))

    def uuid(self, value):
        """
        Validates that the field under validation must be a valid UUID.

        Args:
            value: The value to validate.

        Returns:
            bool: True if the value is a valid UUID, False otherwise.
        """
        try:
            uuid_obj = uuid.UUID(value, version=1)  # Can check for other versions as needed
            return str(uuid_obj) == value
        except ValueError:
            return False

    def apply_rule(self, field, rule):
        """
        Apply a specific rule to a field value.

        Args:
            field (str): The field name in the data.
            rule (str): The validation rule with optional parameters.

        Raises:
            ValueError: If the validation rule does not exist.
        """

        # Retrieve the value to be validated.
        value = self.dot_notation_access(field)

        # Parse rule name and parameters.
        rule_parts = rule.split(':')
        rule_name = rule_parts[0]
        param = rule_parts[1] if len(rule_parts) > 1 else None

        # Execute validation using reflection.
        try:
            value_repr = value if not isinstance(value, str) else f"'{value}'"
            params = f", {param}" if param else ''
            result = eval(f"self.{rule_name}({value_repr}{params})")
        except Exception:
            raise ValueError(f"Undefined validation function '{rule_name}(self, ...)'. Define it within the FormRequest class.")

        # Register the error if validation fails.
        if not result:
            self.add_error(field, rule_name)

    def apply_array_rules(self, field, validations):
        """
        Apply rules to array-type fields in the data.

        Args:
            field (str): The field with array notation to validate.
            validations (list): List of validation rules for each array element.
        """

        # Split field name and subfield.
        array_field, sub_field = field.split('.*.')

        if array_field not in self.data or not isinstance(self.data[array_field], list):
            self.add_error(field, 'list', f"The {field} validation requires {sub_field} to be a list.")
            return

        for index, item in enumerate(self.data[array_field]):
            if not isinstance(item, dict) or sub_field not in item:
                self.add_error(field, 'dict|not none', f"The value of {sub_field} is missing or not a dictionary in {item}")
                continue

            for validation in validations:
                self.apply_rule(f"{array_field}.{index}.{sub_field}", validation)

    def add_error(self, field, rule_name, message: str = None):
        """
        Register an error for a specific field and rule.

        Args:
            field (str): The field where the error occurred.
            rule_name (str): The rule that failed.
            message (str, optional): Custom error message.
        """

        formatted_field = re.sub(r'\.\d+\.', r'.*.', field) + f'.{rule_name}'
        message = self.messages().get(formatted_field, message or f"Validation for {field} failed on {rule_name}.")
        if field not in self.errors:
            self.errors[field] = []
        self.errors[field].append(message)
        if not self.first_error:
            self.first_error = message

    def get_errors(self):
        """
        Generate an error response similar to Laravel's format.

        Returns:
            dict: Contains a summary message of the first error and all field-specific errors.
                The message includes the first error description and, if applicable, an indication
                of the additional number of errors.
        """

        # Total number of errors collected.
        error_count = len(self.errors)

        # If more than one error, append information about additional errors.
        add_info = f" (and {error_count - 1} more {'errors' if error_count > 2 else 'error'})" if error_count > 1 else ''

        # Return the formatted error message and error details.
        return {
            "message": f"{self.first_error}{add_info}",
            "errors": self.errors
        }

