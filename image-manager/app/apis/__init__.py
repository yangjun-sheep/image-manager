from flask import Blueprint
admin_bp = Blueprint('admin_api', __name__)
from app.apis import admin_apis
image_bp = Blueprint('image_api', __name__)
from app.apis import image_apis
