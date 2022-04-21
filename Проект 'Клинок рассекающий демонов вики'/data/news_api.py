import flask
from flask import jsonify, request

from data import db_session
from data.demons import Demons
from data.news import News
from data.others import Others
from data.suzhet import Suzhet

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/news')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(News).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('title', 'age', 'status', 'content', 'user.name'))
                 for item in news]
        }
    )


@blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'news': news.to_dict(only=(
                'title', 'age', 'status', 'content', 'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    news = News(
        title=request.json['title'],
        age=request.json['age'],
        status=request.json['status'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/suzhets')
def get_suzhets():
    db_sess = db_session.create_session()
    suzhet = db_sess.query(Suzhet).all()
    return jsonify(
        {
            'suzhet':
                [item.to_dict(only=('title', 'content', 'user.name'))
                 for item in suzhet]
        }
    )


@blueprint.route('/api/suzhets/<int:suzhets_id>', methods=['GET'])
def get_one_suzhets(suzhets_id):
    db_sess = db_session.create_session()
    suzhet = db_sess.query(Suzhet).get(suzhets_id)
    if not suzhet:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'suzhet': suzhet.to_dict(only=(
                'title', 'content', 'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/suzhets', methods=['POST'])
def create_suzhets():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    suzhet = Suzhet(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(suzhet)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/suzhets/<int:suzhets_id>', methods=['DELETE'])
def delete_suzhets(suzhets_id):
    db_sess = db_session.create_session()
    suzhet = db_sess.query(Suzhet).get(suzhets_id)
    if not suzhet:
        return jsonify({'error': 'Not found'})
    db_sess.delete(suzhet)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/demons')
def get_demons():
    db_sess = db_session.create_session()
    demons = db_sess.query(Demons).all()
    return jsonify(
        {
            'demons':
                [item.to_dict(only=('title', 'age', 'status', 'content', 'user.name'))
                 for item in demons]
        }
    )


@blueprint.route('/api/demons/<int:demons_id>', methods=['GET'])
def get_one_demons(demons_id):
    db_sess = db_session.create_session()
    demons = db_sess.query(Demons).get(demons_id)
    if not demons:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'demons': demons.to_dict(only=(
                'title', 'age', 'status', 'content', 'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/demons', methods=['POST'])
def create_demons():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    demons = Demons(
        title=request.json['title'],
        age=request.json['age'],
        status=request.json['status'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(demons)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/demons/<int:demons_id>', methods=['DELETE'])
def delete_demons(demons_id):
    db_sess = db_session.create_session()
    demons = db_sess.query(Demons).get(demons_id)
    if not demons:
        return jsonify({'error': 'Not found'})
    db_sess.delete(demons)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/others')
def get_others():
    db_sess = db_session.create_session()
    others = db_sess.query(Others).all()
    return jsonify(
        {
            'others':
                [item.to_dict(only=('title', 'age', 'status', 'content', 'user.name'))
                 for item in others]
        }
    )


@blueprint.route('/api/others/<int:others_id>', methods=['GET'])
def get_one_others(others_id):
    db_sess = db_session.create_session()
    others = db_sess.query(Others).get(others_id)
    if not others:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'others': others.to_dict(only=(
                'title', 'age', 'status', 'content', 'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/others', methods=['POST'])
def create_others():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    others = Others(
        title=request.json['title'],
        age=request.json['age'],
        status=request.json['status'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(others)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/others/<int:others_id>', methods=['DELETE'])
def delete_others(others_id):
    db_sess = db_session.create_session()
    others = db_sess.query(Others).get(others_id)
    if not others:
        return jsonify({'error': 'Not found'})
    db_sess.delete(others)
    db_sess.commit()
    return jsonify({'success': 'OK'})