import azure.functions as func
import logging
import flask
import os

app = flask.Flask(
    __name__,
    static_folder="frontend",
    static_url_path="",   
    template_folder="frontend/templates"   
)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

@app.route('/')
def index():
    return flask.render_template("choose.html")

@app.route('/galery')
def chose():
    return flask.render_template("galery.html")

@app.route('/contact')
def contact():
    return flask.render_template("contact.html")

@app.route('/about')
def about():
    return flask.render_template("about.html")

@app.route('/info')
def info():
    return flask.render_template("info.html")

# TODO: make and icon
@app.route('/favicon.ico') 
def favicon(): 
    return flask.send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def page_not_found(e):
    return flask.render_template('404.html'), 404



# https://www.youtube.com/watch?v=ldFJBzSH5cM&list=LL&index=1&t=643s
# https://learn.microsoft.com/en-us/samples/azure-samples/flask-app-on-azure-functions/azure-functions-python-create-flask-app/
# https://learn.microsoft.com/en-us/azure/azure-functions/functions-how-to-github-actions?tabs=linux%2Cpython&pivots=method-template
# https://www.youtube.com/watch?v=88Kza0eidcE
# https://www.youtube.com/watch?v=MvbCAacLkww
# https://learn.microsoft.com/en-us/azure/app-service/manage-custom-dns-buy-domain
