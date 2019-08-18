import asyncio
import base64
import urllib.parse

from starlette.types import Message, ASGIApp

from uvicorn.lifespan import Lifespan

class LambdaFunction:

    def __init__(self, asgi: ASGIApp):
        self._asgi = asgi

    def lambda_handler(self, event, context):
        loop = asyncio.get_event_loop()
        lifespan = Lifespan(self._asgi)
        loop.create_task(lifespan.run())
        loop.run_until_complete(lifespan.wait_startup())

        connection_scope = self.get_connection_scope(
            event=event,
            context=context
        )

        async def _receive() -> Message:
            body = event['body']
            if event['isBase64Encoded']:
                body = base64.standard_b64decode(body)
            return {
                'type': 'http.request',
                'body': body,
                'more_body': False
            }

        response = {}

        async def _send(message: Message) -> None:
            if message['type'] == 'http.response.start':
                response["statusCode"] = message['status']
                response["isBase64Encoded"] = False
                response["headers"] = {k.decode('utf-8'):v.decode('utf-8') for k, v in message['headers']}
            if message['type'] == 'http.response.body':
                response["body"] = message['body'].decode('utf-8')

        asgi = self._asgi(connection_scope)
        loop.run_until_complete(asgi(_receive, _send))
        loop.run_until_complete(lifespan.wait_shutdown())

        return response

    def _unwrap_multi_value_parameters(self, parameters: dict):
        for key, value in parameters.items():
            if isinstance(value, list):
                for sub_value in value:
                    yield key, sub_value

            else:
                yield key, value

    def get_query_string(self, event: dict):
        parameters: dict = event['queryStringParameters']
        parameters.update(event['multiValueQueryStringParameters'])

        pairs = list(self._unwrap_multi_value_parameters(parameters))

        return urllib.parse.urlencode(pairs)

    def get_connection_scope(self, event, context):
        return {
            'type': 'http',
            'http_version': '1.1',
            'scheme': 'http',
            'method': event['httpMethod'],
            'root_path': '',
            'path': event['path'],
            'query_string': self.get_query_string(event),
            'headers': event['headers'].items(),
            'x-aws-lambda': {
                'requestContext': event['requestContext'],
                'lambdaContext': context
            }
        }
