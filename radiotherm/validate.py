import json

def validate_response(response, content=None):
    """
    raises AttributeError if the HTTP response code is not 200, or if the value
    returned by the server indicates an error.

    :param response:    the response returned by a call to urllib.request.urlopen
    :type response:     file-like object
    :param content:     the JSON-deserialized value returned by the server.
                        This is required if the response was "read" prior to
                        calling this method.
    :type content:      any iterable collection 
    :returns:           tuple of the validated response and content
    :raises:            AttributeError
    """
    if response.getcode() != 200:
        raise AttributeError('HTTP code %d. %s' % (response.code, response.msg))

    if content is None:
        content = json.loads(response.read().decode('utf-8'))

    for error_field in ('error_msg', 'error'):
        if error_field in content:
            raise AttributeError('Error message from thermostat: %s' % content[error_field])
    return response, content


def validate_tstat_response(response, content=None):
    """
    raises AttributeError if the HTTP response code is not 200, or if the value
    returned by the server for /tstat indicates an error.

    :param response:    the response returned by a call to urllib.request.urlopen
    :type response:     file-like object
    :param content:     the JSON-deserialized value returned by the server.
                        This is required if the response was "read" prior to
                        calling this method.
    :type content:      any iterable collection
    :returns:           tuple of the validated response and content
    :raises:            AttributeError
    """
    response, content = validate_response(response, content)
    for field in ('tmode', 'temp'):
        if content[field] == -1:
            raise AttributeError('Transient error from thermostat. You should probably just retry.')
    return response, content
