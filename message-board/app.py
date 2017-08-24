import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

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


@app.route('/api/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by('created_at desc').all()
    return jsonify([message.to_dict() for message in messages])


@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    msg = Message(name=data['name'], text=data['text'])
    db.session.add(msg)
    db.session.commit()
    return jsonify(ok=True)


if __name__ == '__main__':
    app.run(debug=True)
