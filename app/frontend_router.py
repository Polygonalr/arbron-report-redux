from flask import Blueprint, request, abort, render_template, redirect, url_for
from app.models import Report, HashResult
import os
import shutil
import tempfile
import math

frontend_blueprint = Blueprint('frontend_router', __name__)

@frontend_blueprint.route("/")
def index():
    return redirect(url_for("frontend_router.ShowAllReports"))

@frontend_blueprint.route("/app/report", methods=['GET'])
def ShowAllReports():
    page_no = request.args.get('page')
    if page_no == None:
        page_no = 1
    report_query = Report.query.order_by(Report.creation_datetime.desc()).paginate(page_no, 10, False)
    return render_template(
        'show_all_reports.html',
        report_items = report_query.items,
        total = report_query.total,
        page_no = page_no,
        max_page = math.ceil(report_query.total/10)
    )

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
