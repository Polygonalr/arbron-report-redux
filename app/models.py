'''
models.py contains most of the code that interacts with the database backend.
'''
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv
import os

from app import db

load_dotenv()

# Declaration of HashResult model to be used with SQLAlchemy
class HashResult(db.Model):
    hash = db.Column(db.String(128), primary_key=True)
    detected = db.Column(db.Boolean, nullable=False)
    md5 = db.Column(db.String(32), nullable=True)
    report_id = db.Column(db.Integer, db.ForeignKey("report.id"), nullable=False)

    def save(self):
        if self.hash == None:
            db.session.add(self)
        return db.session.commit()

    def __repr__(self):
        return "<HashResult {}>".format(self.hash)

# Declaration of Report model to be used with SQLAlchemy
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    creation_datetime = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    hash_results = db.relationship("HashResult", backref=db.backref('report'), lazy=True)

    def save(self):
        if self.id == None:
            db.session.add(self)
        return db.session.commit()

    def destroy(self):
        db.session.delete(self)
        return db.session.commit()

    def __repr__(self):
        return "<Report {}>".format(self.name)

# Takes in assessments dict, report_name and (optional) report_datetime
# Stores new HashResults in database
# Returns None if the newly generated report does not contain any hashes
#   (i.e. the Report object contains no HashResults as the HashResults within assessments parameter already exists under another Report within the database)
# Returns Report object otherwise
def update_database(assessments: dict, report_name: str, report_datetime: str = None):
    # Check whether report with provided report_name exists, create if not
    report = Report.query.filter_by(name=report_name).first()
    if report == None:
        report = Report(name=report_name)
        if report_datetime != None:
            utcdatetime = datetime.strptime(report_datetime, "%Y-%m-%d %H:%M:%S.%f%z")
            report.creation_datetime = utcdatetime.astimezone(timezone("Asia/Singapore"))
        report.save()

    for assessment in assessments:
        # for each hash, check whether exists already
        same_hash = HashResult.query.filter_by(hash=assessment['hash'])
        if(same_hash.count()==0):
            new_hash_result = HashResult(
                hash = assessment['hash'],
                detected = assessment['detected'],
                md5 = assessment['md5'],
                report_id = report.id
            )
            db.session.add(new_hash_result)
    db.session.commit()

    # Reload the report object (not too sure whether needed?)
    report = Report.query.filter_by(name=report_name).first()
    if(len(report.hash_results) == 0):
        report.destroy()
        return None
    return report

