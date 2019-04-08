Create Python async AWS Lambda functions with Starlette.

Currently supports exposing Starlette routes via ALB.

How to use Starlette Lambda with FastAPI:

 .. code-block:: python

    import json

    from starlette_lambda.aws import LambdaFunction
    from fastapi import FastAPI

    app = FastAPI()


    @app.get("/")
    def read_root():
        return {"Hello": "World"}


    @app.get("/items/{item_id}")
    def read_item(item_id: int, q: str = None):
        return {"item_id": item_id, "q": q}


    handler = LambdaFunction(app).lambda_handler
