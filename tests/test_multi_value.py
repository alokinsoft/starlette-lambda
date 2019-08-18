from starlette.applications import Starlette

from starlette_lambda.aws import LambdaFunction


def test_multi_value():
    query_string = LambdaFunction(asgi=Starlette()).get_query_string(event={
        'queryStringParameters': {'make': 'TOYOTA', 'zip_code': '65301'},
        'multiValueQueryStringParameters': {
            'zip_code': ['02368', '65301']
        }
    })

    assert query_string == 'make=TOYOTA&zip_code=02368&zip_code=65301'


def test_pseudo_multi_value():
    query_string = LambdaFunction(asgi=Starlette()).get_query_string(event={
        'queryStringParameters': {'make': 'TOYOTA', 'zip_code': '65301'},
        'multiValueQueryStringParameters': {
            'zip_code': ['02368']
        }
    })

    assert query_string == 'make=TOYOTA&zip_code=02368'
