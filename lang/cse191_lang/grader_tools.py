grader_tools = {}

def tool(f):
    grader_tools[f.__name__] = f
    return f

@tool
def percentage(x, y):
    """
    Convert x/y into a percentage. Useful for calculating success rate

    Args:
        x (int)
        y (int)

    Returns:
        str: percentage formatted into a string
    """
    return '%.2f%%' % (100 * x / y)
