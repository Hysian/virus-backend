#!/usr/bin/env python
# coding: utf-8

"""
 Created by 仙书 on 2020/1/23
"""
from flask import jsonify, request, Response
from models import Count, Article
from app import create_app, cache
from sqlalchemy import desc
import time

app = create_app()


@app.route('/count')
@cache.cached(timeout=30, query_string=True)
def base_api():
    area = request.args.get('area')
    if not area:
        area = '全国'
    count = Count.query.filter(Count.area_name == area).first()
    print(request.args)
    data_type = request.args.get('data')
    data = {
        "confirm":count.confirm_case,
        "probable":count.probable_case,
        "cure":count.cure_case,
        "dead":count.dead_case
    }
    
    if data_type in data:
        return Response(response=str(data[data_type]))
    else:
        return jsonify(data)

@app.route('/count/list')
@cache.cached(timeout=30, query_string=True)
def count_list():
    counts = Count.query.filter(Count.area_type == 'province').order_by(desc(Count.confirm_case)).all()
    data = []
    for count in counts:
        data.append({
            "name": count.area_name,
            "confirm": count.confirm_case,
            "probable": count.probable_case,
            "cure": count.cure_case,
            "dead": count.dead_case,
            "new": count.new_case
        })
    return jsonify(data)


@app.route('/article/list')
@cache.cached(timeout=30, query_string=True)
def article_list():
    articles = Article.query.order_by(desc(Article.time)).all()
    data = []
    for article in articles:
        data.append({
            "title": article.title,
            "detail": article.detail,
            "time": article.time.strftime("%Y-%m-%d %H:%M:%S"),
            "link": article.link
        })
    return jsonify(data)


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True,port=8100)