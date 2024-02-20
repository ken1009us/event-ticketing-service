from datetime import datetime


def validate_int(input_str, field_name="value"):
    try:
        return True, int(input_str)
    except ValueError:
        return False, f"Error: {field_name} must be an integer."


def validate_datetime(
    input_str, field_name="date and time", date_format="%Y-%m-%d %H:%M:%S"
):
    try:
        return True, datetime.strptime(input_str, date_format)
    except ValueError:
        return False, f"Error: {field_name} must be in the format {date_format}."
