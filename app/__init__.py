import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

import rq
from elasticsearch import Elasticsearch
from flask import current_app, Flask, request
from flask_babel import Babel, lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

from config import Config


babel = Babel()
bootstrap = Bootstrap()
db = SQLAlchemy()
login = LoginManager()
migrate = Migrate()
mail = Mail()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    babel.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    moment.init_app(app)

    login.login_view = 'auth.login'
    login.login_message = _l('Please log in to access this page.')

    app.elasticsearch = Elasticsearch(
        [app.config['ELASTICSEARCH_HOST']]
    ) if app.config['ELASTICSEARCH_HOST'] else None

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Logging
    if not app.debug and not app.testing:
        # Email errors
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = () if app.config['MAIL_USE_TLS'] else None

            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-replace@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'],
                subject='Microblog Error',
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # Log to file
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/microblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

    return app


from app import models


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])
