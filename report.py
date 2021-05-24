#TODO Formating of report (colors, column widths)

import xlsxwriter
import os
import uuid
import shutil
import tempfile
import weakref
from models import HashResult, Report

# Low level function to generate xlsx from assessment dict
def generate_report_from_dict(assessments, dirpath):
    report_full_path = dirpath + "/{}.xlsx".format(uuid.uuid4().hex)
    wb = xlsxwriter.Workbook(report_full_path)
    ws = wb.add_worksheet()
    # Writing of the table headings
    ws.write(0,0,"Hash")
    ws.write(0,1,"Detected")
    ws.write(0,2,"MD5 Eqv")
    # Writing of the data to table body
    row, col = 1, 0
    bool_string_translation = { True:"Yes", False:"No" }
    for assessment in assessments:
        ws.write(row,col,assessment['hash'])
        ws.write(row,col+1,bool_string_translation[assessment['detected']])
        ws.write(row,col+2,assessment['md5'])
        row += 1
    wb.close()
    return report_full_path

# Low level function to generate xlsx from all the hashes within the database
def generate_report_from_all(dirpath):
    report_full_path = dirpath + "/{}.xlsx".format(uuid.uuid4().hex)
    wb = xlsxwriter.Workbook(report_full_path)
    ws = wb.add_worksheet()
    # Writing of the table headings
    ws.write(0,0,"Hash")
    ws.write(0,1,"Detected")
    ws.write(0,2,"MD5 Eqv")
    ws.write(0,3,"Report Name")
    ws.write(0,4,"Datetime")
    # Writing of the data to table body
    row, col = 1, 0
    hashes = HashResult.query.all()
    for hash in hashes:
        ws.write(row,col,hash.hash)
        ws.write(row,col+1,hash.detected)
        ws.write(row,col+2,hash.md5)
        ws.write(row,col+3,hash.report.name)
        ws.write(row,col+4,hash.report.creation_datetime)
        row += 1
    wb.close()
    return report_full_path
