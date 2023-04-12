import logging
from uuid import uuid4


# decorator
from functools import wraps
def get_and_check_workflow_metadata(vhandler):
    '''
    Use it to ensure to get a usable workflow_metadata.
    The decorated function should have: "workflow_metadata" as its input argument,
    and "id" as input argument or in the request.
    For example: def f(id, a, b, workflow_metadata={}) 
    '''
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            # print(func.__name__)      # 输出 'f'
            # print(func.__doc__)       # 输出 ''' ... '''
            print('try to get', kwargs.get('id', request.args.get('id')))
            workflow_metadata = vhandler._validate_workflow_and_get_metadata(kwargs.get('id', request.args.get('id')))
            if workflow_metadata:
                return func(*args, workflow_metadata=workflow_metadata, **kwargs)
            else:
                # return 'Workflow not found', 404
                return make_response(render_template('index.html', message='Workflow not found'))
        return wrap
    return decorator

def debug_log(func):
    '''
    print function input & return for debug 
    '''
    @wraps(func)
    def wrap(*args, **kwargs):
        # print(func.__name__)      # 输出 'f'
        logging.info(f'{func.__name__} inputs: {args} {kwargs}')
        ret = func(*args, **kwargs)
        logging.info(f'{func.__name__} returns: {ret}')
        return ret
    return wrap

