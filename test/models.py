class Admin(User):
    __tablename__ = 'Admin'
    id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)


class Search(db.Model):
    __tablename__='Search'
    sid = db.Column(db.Integer, primary_key=True)  #Search history ID
    id = db.Column(db.Integer, db.ForeignKey('User.id'))
    item = db.Column(db.String(64))
    time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Search %r>' % self.sid

class Post(db.Model):
    __tablename__='Post'
    tid = db.Column(db.Integer, primary_key=True)  # Post transaction ID
    uid = db.Column(db.Integer, db.ForeignKey('User.id'))  #UserID
    c1_item = db.Column(db.Integer, db.ForeignKey('Currency.cid'))    # The item user wants to sell
    c2_item = db.Column(db.Integer, db.ForeignKey('Currency.cid'))     # The item user wants to get
    c1_number = db.Column(db.Integer)
    c2_number = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    def __init__(self, uid, c1_item, c2_item, c1_number, c2_number, time):
        self.uid = uid
        self.c1_item = c1_item
        self.c2_item = c2_item
        self.c1_number = c1_number
        self.c2_number = c2_number

    def __repr__(self):
        return '<Post %r>' % self.tid