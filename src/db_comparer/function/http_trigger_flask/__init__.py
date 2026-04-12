import azure.functions as func
import logging
import flask
import os

app = flask.Flask(
    __name__ 
)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

@app.route('/')
def index():
    return 'Hello from Azure Functions + Flask!'

