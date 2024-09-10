from flask_sqlalchemy import SQLAlchemy
import datetime



db = SQLAlchemy()



class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gigid = db.Column(db.String, nullable=False)
    reviewerid = db.Column(db.String, nullable=False)
    orderid = db.Column(db.String, nullable=False)
    sellerid = db.Column(db.String, nullable=False)
    review = db.Column(db.Text, nullable=False)
    reviewerimage = db.Column(db.String, nullable=False)
    reviewerusername = db.Column(db.String, nullable=False)
    country = db.Column(db.String, nullable=False)
    reviewtype = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, default=0, nullable=False)
    createdat = db.Column(db.DateTime, default=datetime.datetime.now())


    def __init__(self, gigid, reviewerid, orderid, sellerid, review, reviewerimage, reviewerusername, country, reviewtype, rating, createdat):
        self.gigid = gigid
        self.reviewerid = reviewerid
        self.orderid = orderid
        self.sellerid = sellerid
        self.reviewerimage = reviewerimage
        self.country = country
        self.reviewtype = reviewtype
        self.rating = rating
        self.createdat = createdat
        self.reviewerusername = reviewerusername
        self.review = review


