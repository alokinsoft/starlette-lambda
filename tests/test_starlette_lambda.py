from starlette_lambda import __version__

class ClientContext(object):
    __slots__ = ['custom', 'env', 'client']


def make_obj_from_dict(_class, _dict, fields=None):
    if _dict is None:
        return None
    obj = _class()
    set_obj_from_dict(obj, _dict)
    return obj


def set_obj_from_dict(obj, _dict, fields=None):
    if fields is None:
        fields = obj.__class__.__slots__
    for field in fields:
        setattr(obj, field, _dict.get(field, None))


class LambdaContext(object):
    def __init__(self, invokeid=None, context_objs=None, client_context=None, invoked_function_arn=None):
        self.aws_request_id = invokeid
        # self.log_group_name = os.environ['AWS_LAMBDA_LOG_GROUP_NAME']
        # self.log_stream_name = os.environ['AWS_LAMBDA_LOG_STREAM_NAME']
        # self.function_name = os.environ["AWS_LAMBDA_FUNCTION_NAME"]
        # self.memory_limit_in_mb = os.environ['AWS_LAMBDA_FUNCTION_MEMORY_SIZE']
        # self.function_version = os.environ['AWS_LAMBDA_FUNCTION_VERSION']
        self.invoked_function_arn = invoked_function_arn

        self.client_context = make_obj_from_dict(ClientContext, client_context)
        if self.client_context is not None:
            self.client_context.client = None
        self.identity = None

    def get_remaining_time_in_millis(self):
        return None

    def log(self, msg):
        str_msg = str(msg)
        print(str_msg)
        # lambda_runtime.send_console_message(str_msg, byte_len(str_msg))

def test_version():
    assert __version__ == '0.1.0'
