import re

ALLOWED_EXTENSIONS = ['csv', 'xlxs']

def convert_to_array_or_dict(cell_value):
    if isinstance(cell_value, str):
        # Check for square brackets '[ ]'
        if '[' in cell_value and ']' in cell_value:
            # Extract content inside square brackets and convert to array
            content = re.search(r'\[(.*?)\]', cell_value).group(1)
            elements = [element.strip() for element in content.split(',')]
            return elements
        # Check for curly brackets '{ }'
        elif '{' in cell_value and '}' in cell_value:
            # Extract content inside curly brackets and convert to dictionary
            content = re.search(r'\{(.*?)\}', cell_value).group(1)
            pairs = [pair.strip().split(':') for pair in content.split(',')]
            dictionary = {pair[0].strip(): pair[1].strip() for pair in pairs}
            return dictionary
        # Check for comma-separated values
        elif ',' in cell_value:
            # Split the cell value by commas and strip whitespace from each element
            elements = [element.strip() for element in cell_value.split(',')]
            return elements
    return cell_value

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


