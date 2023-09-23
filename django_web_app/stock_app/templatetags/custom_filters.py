# Import the Django template library
from django import template

# Initialize a template library instance
register = template.Library()

# Define a custom filter named 'multiply'
@register.filter
def multiply(value, arg):
    # Convert both the value and argument to float and multiply them
    result = float(value) * float(arg)
    # Round the result to 2 decimal places and return
    return round(result, 2)

# Define another custom filter named 'in_millions'
@register.filter
def in_millions(value, decimal_places=0):
    # Convert the given value to millions
    value_in_millions = float(value) / 1_000_000
    # Format the value to the specified number of decimal places,
    # adding commas as needed
    formatted_value = '{:,.{prec}f}'.format(value_in_millions, prec=decimal_places)
    # Return the formatted value
    return formatted_value
