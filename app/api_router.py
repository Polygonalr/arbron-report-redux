'''
api_router.py contains routes for API calls from arbron-frontend
'''
from flask import Blueprint, request, abort, send_file, jsonify
from app.report import generate_report_from_dict, generate_report_from_all
from app.models import Report, update_database
import os
import io
import shutil
import tempfile
import weakref
import re

api_blueprint = Blueprint('api_router', __name__)

# Class which is in-charge of removing temporary files after send_file completes
# class FileRemover(object):
    # def __init__(self):
        # self.weak_references = dict()  # weak_ref -> filepath to remove

    # def cleanup_once_done(self, response, filepath):
        # wr = weakref.ref(response, self._do_cleanup)
        # self.weak_references[wr] = filepath

    # def _do_cleanup(self, wr):
        # filepath = self.weak_references[wr]
        # print('Deleting %s' % filepath)
        # shutil.rmtree(filepath, ignore_errors=True)

# file_remover = FileRemover()

# Removes redundant fields within the assessment dict
def simplify_dict(assessment):
    if assessment['translation'] == None:
        assessment['md5'] = ""
    else:
        assessment['md5'] = assessment['translation']['md5']
    del assessment['translation']
    return assessment

# Replaces invalid characters for Windows filename with '-'
def clean_xlsx_file_name(report_name):
    return re.sub(r'[<>:"/\|?*]', '-', report_name) + ".xlsx"

# Handles upload of hash assessments
# Updates the database based on report_name, then generates and sends the Xlsx report
@api_blueprint.route('/report/<report_name>', methods=['PUT'])
def PutReport(report_name="unspecified"):
    if not request.is_json:
        abort(500)
    assessments = request.get_json()
    assessments = list(map(simplify_dict, assessments))

    # Store the report in the db
    update_database(assessments=assessments, report_name=report_name)

    # Create a temp directory and generate the xlsx report in it
    #tempdir = tempfile.mkdtemp()

    # Generate the xlsx file, send it and then cleanup
    #generated_report_file_path = generate_report_from_dict(assessments,tempdir)
    #xlsx_file_name = re.sub(r'[<>:"/\|?*]', '-', report_name) + ".xlsx"
    #resp = send_file(generated_report_file_path, as_attachment=True, attachment_filename=clean_xlsx_file_name(report_name))
    #file_remover.cleanup_once_done(resp, tempdir)
    #return resp

    # Create a temp directory and generate the xlsx report in it and store it in memory (return_data)
    with tempfile.TemporaryDirectory() as tempdir:
        generated_report_file_path = generate_report_from_dict(assessments,tempdir)
        return_data = io.BytesIO()
        with open(generated_report_file_path, 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)
        
    return send_file(
        return_data, 
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        attachment_filename=clean_xlsx_file_name(report_name),
        as_attachment=True
    )


# Given a report_name, handles download of the Xlsx report
@api_blueprint.route('/report/<report_name>', methods=['GET'])
def GetXlsxReport(report_name="unspecified"):
    # Create a temp directory and generate the xlsx report in it
    tempdir = tempfile.mkdtemp()

    # Check whether report exists, 404 if not.
    report = Report.query.filter_by(name=report_name).first()
    if report == None:
        abort(404)
    hash_results = report.hash_results

    # Convert all the objects to dict to be used in the report generation function
    assessments = []
    for hash_result in hash_results:
        assessment = hash_result.__dict__
        assessments.append(assessment)

    with tempfile.TemporaryDirectory() as tempdir:
        generated_report_file_path = generate_report_from_dict(assessments,tempdir)
        return_data = io.BytesIO()
        with open(generated_report_file_path, 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)

    return send_file(
        return_data,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        attachment_filename=clean_xlsx_file_name(report_name),
        as_attachment=True
    )
    
    # Generate the xlsx file, send it and then cleanup
    # generated_report_file_path = generate_report_from_dict(assessments,tempdir)
    # resp = send_file(generated_report_file_path, as_attachment=True, attachment_filename=clean_xlsx_file_name(report_name))
    # file_remover.cleanup_once_done(resp, tempdir)
    # return resp

# Collates all reports into a single master Xlsx, sends it afterwards.
@api_blueprint.route('/all-report', methods=['GET'])
def CollateAllXlsxReports():
    # Create a temp directory to generate the xlsx report
    with tempfile.TemporaryDirectory() as tempdir:
        generated_report_file_path = generate_report_from_all(tempdir)
        return_data = io.BytesIO()
        with open(generated_report_file_path, 'rb') as fo:
            return_data.write(fo.read())
        return_data.seek(0)

    return send_file(
        return_data,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        attachment_filename='all-report.xlsx',
        as_attachment=True
    )

    # tempdir = tempfile.mkdtemp()
    # generated_report_file_path = generate_report_from_all(tempdir)
    # resp = send_file(generated_report_file_path, as_attachment=True, attachment_filename="all-report.xlsx")
    # file_remover.cleanup_once_done(resp, tempdir)
    # return resp

@api_blueprint.route('/migrate-json', methods=['POST'])
def MigrateJson():
    if not request.is_json:
        abort(500)
    report_list = request.get_json()
    for report in report_list:
        update_database(
            assessments=report['assessments'],
            report_name=report['report_name'],
            report_datetime=report['report_datetime']
        )
    return jsonify(success=True)
