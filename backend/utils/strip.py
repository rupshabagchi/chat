import re

def strip_response(_response):
    pattern = r'\"\"\"(.*?)\"\"\"'

    replies = re.findall(pattern, _response, re.DOTALL)

    response = None
    for idx, reply in enumerate(replies, start=1):
        response = f"Question {idx}: {reply.strip()}"

    if response is not None:     
        return response
    
    return _response

