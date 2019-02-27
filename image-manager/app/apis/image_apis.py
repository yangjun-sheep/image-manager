# coding:utf8

import sys
from flask import request, jsonify, current_app
from sqlalchemy import and_
from app.models.models import (
    Category,
    Image,
    Recommendation
)
from app.apis import image_bp
from app import db

reload(sys)
sys.setdefaultencoding('utf-8')
db_session = db.session


@image_bp.route('/category/list', methods=['GET'])
def get_category_list():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    page_number = int(request.args.get('page_number', 1))
    page_size = int(request.args.get('page_size', 20))
    page = Category.query.filter().paginate(page_number, page_size)
    category_list = [row.to_dict() for row in page.items]
    ret = {
        'status_code': status_code,
        'message': message,
        'data': category_list,
        'total_page': page.pages,
        'total_number': page.total
    }
    return jsonify(ret)


@image_bp.route('/image/list', methods=['GET'])
def get_image_list():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    category_id = request.args.get('category_id')
    page_number = int(request.args.get('page_number', 1))
    page_size = int(request.args.get('page_size', 20))

    ands = []
    if category_id:
        ands.append(and_(Category.id == category_id))

    page = db_session.query(Image, Category).filter(
        Image.is_deleted == False,
        Image.category_id == Category.id
    ).filter(
        *ands
    ).paginate(page_number, page_size)

    image_list = []
    for row in page.items:
        image = row.Image.to_dict()
        image['category'] = row.Category.to_dict()
        image_list.append(image)

    ret = {
        'status_code': status_code,
        'message': message,
        'data': image_list,
        'total_page': page.pages,
        'total_number': page.total
    }
    return jsonify(ret)


@image_bp.route('/recommendation/list', methods=['GET'])
def get_recommendation_list():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    page_number = int(request.args.get('page_number', 1))
    page_size = int(request.args.get('page_size', 20))
    page = Recommendation.query.filter().paginate(page_number, page_size)

    recommendation_list = []
    for row in page.items:
        recommendation = row.to_dict()
        recommendation['images'] = [row.to_dict() for row in row.get_images()]
        recommendation_list.append(recommendation)

    ret = {
        'status_code': status_code,
        'message': message,
        'data': recommendation_list,
        'total_page': page.pages,
        'total_number': page.total
    }
    return jsonify(ret)
