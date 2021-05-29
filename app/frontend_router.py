from flask import Blueprint, request, abort, render_template
from app.models import Report, HashResult
import os
import shutil
import tempfile
import weakref

frontend_blueprint = Blueprint('frontend_router', __name__)

@frontend_blueprint.route('/app/report/<report_name>', methods=['GET'])
def GetReport(report_name='unspecified'):
    report = Report.query.filter_by(name=report_name).first()
    if report == None:
        abort(404)
    assessments = report.hash_results
    return render_template(
        'get_report.html',
        assessments=report.hash_results,
        report_name=report.name
    )
