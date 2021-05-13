# celery-flask integration poc

To integrate celery with flask we have to create a function for celery confuguration as bellow:

    def make_celery(app):
        celery = Celery(
            app.import_name,
            backend=app.config['CELERY_RESULT_BACKEND'],
            broker=app.config['CELERY_BROKER_URL']
        )
        celery.conf.update(app.config)

        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        celery.Task = ContextTask
        return celery            

Next, we have to create a object of flask:

    flask_app = Flask(__name__)

We need update the backend confuguration of celery :

    flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
    )    

Next, We need to intialize the celery app by passing the flask_app object as a argument:

    cel = make_celery(flask_app)

Now We have to create route and need to call the task inside the route like below:

    @flask_app.route("/xvb", methods=['GET'])
    def start_job():
        result = name.delay("rahul")
        result.wait()
        return 'Celery integrated with flask is up and running!! cheers'

    @cel.task(name="celery_flask.name")
    def name(name):
        return name 

To run the app, we need to run the app in two differnt terminal one is as flask app another is as celery app:

    celery -A celery_flask.cel worker --loglevel=info

    python3 celery_flask.py

 **   celery_flask is the name of the file or celery project its calling "cel" which is creating the celery app inside code.
