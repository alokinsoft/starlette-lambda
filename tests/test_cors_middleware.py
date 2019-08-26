from pprint import pprint

from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response

from starlette_lambda.aws import LambdaFunction

app = Starlette(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.route('/')
async def homepage(request):
    return JSONResponse(
        {'hello': 'world'},
        headers={'X-Hello': 'World'}
    )


handler = LambdaFunction(app).lambda_handler


def test_cors():
    """Check that starlette-lambda works with CORS middleware."""

    # FIXME CORS Middleware adds Access-Control-Allow-Origin header, which
    #   makes it possible for the browser to perform an HTTP request to our API
    #   from the context of another origin. At the moment of writing this
    #   comment, this test fails: the header this middleware is adding is not
    #   present in the response. I was not yet able to ascertain why.
    #   However, a custom X-Hello header, as we can see, DOES appear, which
    #   probably means something is broken specifically related to middleware.

    event = {
        "httpMethod": "GET",
        "path": "/",
        "headers": {
            "Origin": "https://example.com"
        },
        "requestContext": {},

        "queryStringParameters": {
            "hello": "world",
        }
    }

    response = handler(event=event, context={})

    pprint(response)

    headers = response['headers']

    assert 'x-hello' in headers
    assert 'access-control-allow-origin' in headers
