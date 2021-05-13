from flask import Flask
from celery_config import make_celery

flask_app = Flask(__name__)

flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)

cel = make_celery(flask_app)



@flask_app.route("/xvb", methods=['GET'])
def start_job():
    result = name.delay("rahul")
    result.wait()
    return 'Celery integrated with flask is up and running!! cheers'

@cel.task(name="celery_flask.name")
def name(name):
    return name 

if __name__ == "__main__"   :
    flask_app.run(debug=True)   