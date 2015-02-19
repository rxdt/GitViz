import re

def create_cleaned_commit_log(filename):
    input_text = open(filename).read()

    reg = r'(\w+) = ("|\')((\w+( |=))*("|\')\%\w("|\').*("|\'))* \% \(\w+, \w+\)'
    str_format_pattern = re.compile(reg)

    reg2 = r'\w+\.execute\(\w+\)'
    sql_execute_pattern = re.compile(reg2)

    if str_format_pattern.search(input_text) and sql_execute_pattern.search(input_text):
        return True
    return False

    # get json
    # get date from json
    # get files changed from json