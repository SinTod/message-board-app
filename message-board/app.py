#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm as Form
from wtforms.fields import StringField
from wtforms.validators import Required, Length, ValidationError
from werkzeug.datastructures import MultiDict

app = Flask(__name__)
app.config.update(dict(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI='sqlite:///./tmp/test.db'
))
db = SQLAlchemy(app)


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'name': self.name,
            'text': self.text,
            'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
        }


class MessageForm(Form):
    name = StringField(validators=[Required(message=u'请输入您的姓名'), Length(1, 10, message=u'姓名长度要在1-10个字符之间')])
    text = StringField(validators=[Required(message=u'请输入您的留言'), Length(2, 1000, message=u'留言长度要在2~1000字符之间')])

    def validate_name(self, field):
        if Message.query.filter_by(name=field.data).first():
            raise ValidationError(u'名称已存在')

    def creat_message(self):
        msg = Message(name=self.name.data, text=self.text.data)
        db.session.add(msg)
        db.session.commit()
        return msg


@app.route('/api/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by('created_at desc').all()
    return jsonify([message.to_dict() for message in messages])


@app.route('/api/messages', methods=['POST'])
def create_message():
    formdata = MultiDict(request.get_json())
    form = MessageForm(formdata=formdata, obj=None, csrf_enabled=False)

    if not form.validate():
        return jsonify(form.errors), 422
    msg = form.creat_message()
    return jsonify(msg.to_dict()), 201


if __name__ == '__main__':
    app.run(debug=True)
