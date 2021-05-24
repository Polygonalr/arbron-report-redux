from flask import Blueprint, request, abort
from models import Report, HashResult
import os
import shutil
import tempfile
import weakref

frontend_blueprint = Blueprint('frontend_router', __name__)

@api_blueprint.route('/app/report/<report_name>', methods=['GET'])
def GetReport(report_name='unspecified'):
    report = Report.query.filter_by(name=report_name)
    if report == None:
        abort(404)
    assessments = report.hash_results
    return "This route is still WIP!"
