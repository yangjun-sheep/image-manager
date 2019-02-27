# coding:utf8

import os
import sys
import uuid
from flask import request, jsonify, current_app
from sqlalchemy import and_
from app.models.models import (
    Category,
    Image,
    Recommendation,
    RecommendationImageRelation
)
from app.apis import admin_bp
from app import db

reload(sys)
sys.setdefaultencoding('utf-8')
db_session = db.session


@admin_bp.route('/category/add', methods=['POST'])
def add_category():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    data = request.get_json()
    name = data.get('name')
    category = Category(name=name)
    category.save()
    ret = {
        'status_code': status_code,
        'message': message
    }
    return jsonify(ret)


@admin_bp.route('/category/edit', methods=['POST'])
def edit_category():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    data = request.get_json()
    category_id = data.get('category_id')
    name = data.get('name')
    category = Category.query.filter_by(id=category_id).first()
    if category:
        category.name = name
        category.save()
    else:
        status_code = '0001'
        message = 'CATEGORY_NOT_EXIST'
    ret = {
        'status_code': status_code,
        'message': message
    }
    return jsonify(ret)


@admin_bp.route('/category/list', methods=['GET'])
def get_category_list():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    name = request.args.get('name')
    page_number = int(request.args.get('page_number', 1))
    page_size = int(request.args.get('page_size', 20))

    ands = []
    if name:
        ands.append(and_(Category.name.like('%{}%'.format(name))))
    page = Category.query.filter(*ands).paginate(page_number, page_size)
    category_list = [row.to_dict() for row in page.items]
    ret = {
        'status_code': status_code,
        'message': message,
        'data': category_list,
        'total_page': page.pages,
        'total_number': page.total
    }
    return jsonify(ret)


@admin_bp.route('/category/detail', methods=['GET'])
def get_category_detail():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    category_id = request.args.get('category_id')
    category = Category.query.filter_by(id=category_id).first()
    data = {}
    if category:
        data = category.to_dict()
    else:
        status_code = '0001'
        message = 'CATEGORY_NOT_EXIST'
    ret = {
        'status_code': status_code,
        'message': message,
        'data': data
    }
    return jsonify(ret)


@admin_bp.route('/image/add', methods=['POST'])
def add_image():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    category_id = request.form.get('category_id')
    f = request.files['file']
    ext = f.filename.split('.')[-1] if len(f.filename.split('.')) > 1 else ''
    category = Category.query.filter_by(id=category_id).first()
    if category:
        fn = uuid.uuid1()
        if ext:
            fn = '{}.{}'.format(fn, ext)
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], fn))
        image_src = '/static/images/{}'.format(fn)
        image = Image(
            filename=f.filename,
            image_src=image_src,
            category_id=category_id
        )
        image.save()
    else:
        status_code = '0001'
        message = 'CATEGORY_NOT_EXIST'

    ret = {
        'status_code': status_code,
        'message': message
    }
    return jsonify(ret)


@admin_bp.route('/image/delete', methods=['POST'])
def delete_image():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    data = request.get_json()
    image_id = data.get('image_id')
    image = Image.query.filter_by(id=image_id, is_deleted=False).first()
    if image:
        image.is_deleted = True
        image.save()
    ret = {
        'status_code': status_code,
        'message': message
    }
    return jsonify(ret)


@admin_bp.route('/image/batch_delete', methods=['POST'])
def batch_delete_image():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    data = request.get_json()
    image_ids = data.get('image_ids')
    Image.query.filter(Image.id.in_(image_ids), Image.is_deleted == False).update(
        {'is_deleted': 1}, synchronize_session='fetch')
    db_session.commit()
    ret = {
        'status_code': status_code,
        'message': message
    }
    return jsonify(ret)


@admin_bp.route('/image/edit', methods=['POST'])
def edit_image():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    data = request.get_json()
    image_id = data.get('image_id')
    category_id = data.get('category_id')
    image = Image.query.filter_by(id=image_id, is_deleted=False).first()
    category = Category.query.filter_by(id=category_id).first()
    if not image:
        status_code = '0002'
        message = 'IMAGE_NOT_EXIST'
    elif not category:
        status_code = '0001'
        message = 'CATEGORY_NOT_EXIST'
    else:
        image.category_id = category_id
        image.save()
    ret = {
        'status_code': status_code,
        'message': message
    }
    return jsonify(ret)


@admin_bp.route('/image/list', methods=['GET'])
def get_image_list():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    category_name = request.args.get('category_name')
    page_number = int(request.args.get('page_number', 1))
    page_size = request.args.get('page_size', 20)

    ands = []
    if category_name:
        ands.append(and_(Category.name.like('%{}%'.format(category_name))))

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


@admin_bp.route('/recommendation/add', methods=['POST'])
def add_recommendation():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    recommend_date = data.get('recommend_date')[:10]
    image_ids = data.get('image_ids')

    recommendation = Recommendation(
        title=title,
        description=description,
        recommend_date=recommend_date
    )
    recommendation.save()
    for image_id in image_ids:
        relation = RecommendationImageRelation(
            recommendation_id=recommendation.id,
            image_id=image_id
        )
        relation.save()

    ret = {
        'status_code': status_code,
        'message': message,
        'data': recommendation.to_dict()
    }
    return jsonify(ret)


@admin_bp.route('/image/upload', methods=['POST'])
def upload_image():
    status_code, message = '0000', 'SUCCESS'
    ret = {}
    f = request.files.get('file')
    ext = f.filename.split('.')[-1]
    fn = '{}.{}'.format(uuid.uuid1(), ext)
    f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], fn))
    image_src = '/static/images/{}'.format(fn)
    image = Image(
        filename=f.filename,
        image_src=image_src
    )
    image.save()
    ret = {
        'status_code': status_code,
        'message': message,
        'data': image.to_dict()
    }
    return jsonify(ret)


@admin_bp.route('/recommendation/list', methods=['GET'])
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
