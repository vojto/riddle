import json

def response_success(json_format=True):
    ret = {'response': 'success'}

    if json_format:
        return json.dumps(ret)

    return ret

def response_error(reason=None, json_format=True):
    ret = {'response': 'error'}

    if reason:
        ret['reason'] = reason

    if json_format:
        return json.dumps(ret)

    return ret


