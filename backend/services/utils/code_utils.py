import re

def extract_code_html(output:str) -> str:
    """
    Extract code html from a string containing a ```html ... ``` code block
    
    """
    match= re.search(r"```html\s*([\s\S]+ ?)\s*```", output, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return match
    
