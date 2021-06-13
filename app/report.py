import xlsxwriter
import os
import uuid
import shutil
import tempfile
from app.models import HashResult, Report

# Declaration of styles to be used for formatting
detected_style = {
    "font_color": "#006100",
    "bg_color": "#c6efce",
    "font_name": "Consolas"
}
undetected_style = {
    "font_color": "#9c0006",
    "bg_color": "#ffc7ce",
    "font_name": "Consolas"
}
header_style = {
    "bold": True
}
none_style = {
    "italic": True
}
MD5_WIDTH = 36.43
SHA1_WIDTH = 45.71
SHA256_WIDTH = 73.14


# Low level function to generate xlsx from assessment dict
def generate_report_from_dict(assessments, dirpath):
    report_full_path = dirpath + "/{}.xlsx".format(uuid.uuid4().hex)
    wb = xlsxwriter.Workbook(report_full_path)
    detected_format = wb.add_format(detected_style)
    undetected_format = wb.add_format(undetected_style)
    header_format = wb.add_format(header_style)
    ws = wb.add_worksheet()

    # Writing of the table headings
    ws.write(0,0,"Hash", header_format)
    ws.write(0,1,"Detected", header_format)
    ws.write(0,2,"MD5 Eqv", header_format)
    ws.write(0,4,"MD5 to block", header_format)

    # Writing of the data to main table body
    row, col, to_block_row = 1, 0, 1
    bool_string_translation = { True:"Yes", False:"No" }
    longest_hash_len = 0
    for assessment in assessments:
        if assessment['detected']:
            cell_format = detected_format
        else:
            cell_format = undetected_format
        ws.write(row,col,assessment['hash'], cell_format)
        ws.write(row,col+1,bool_string_translation[assessment['detected']], cell_format)
        ws.write(row,col+2,assessment['md5'], cell_format)

        # If assessment indicates undetectable, and md5 available, write to col 4
        if not assessment['detected']:
            if len(assessment['hash']) == 32:
                ws.write(to_block_row, 4, assessment['hash'], undetected_format)
                to_block_row += 1
            elif assessment['md5'] != "":
                ws.write(to_block_row, 4, assessment['md5'], undetected_format)
                to_block_row += 1
        
        # Update longest_hash_len to be used for setting col width
        if len(assessment['hash']) > longest_hash_len:
            longest_hash_len = len(assessment['hash'])
        row += 1
    
    # If there are no hashes to block, indicate as such.
    if to_block_row == 1:
        none_format = wb.add_format(none_style)
        ws.write(1, 4, "None", none_format)

    # Adjustment of column width
    if longest_hash_len <= 32: #md5
        ws.set_column(0, 0, MD5_WIDTH)
    elif longest_hash_len <= 40: #sha1
        ws.set_column(0, 0, SHA1_WIDTH)
    else:
        ws.set_column(0, 0, SHA256_WIDTH)
    ws.set_column(2, 2, MD5_WIDTH)
    ws.set_column(4, 4, MD5_WIDTH)
    wb.close()

    return report_full_path

# Low level function to generate xlsx from all the hashes within the database
def generate_report_from_all(dirpath):
    report_full_path = dirpath + "/{}.xlsx".format(uuid.uuid4().hex)
    wb = xlsxwriter.Workbook(report_full_path)
    detected_format = wb.add_format(detected_style)
    undetected_format = wb.add_format(undetected_style)
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
        if hash['detected']:
            cell_format = detected_format
        else:
            cell_format = undetected_format
        ws.write(row,col,hash.hash, cell_format)
        ws.write(row,col+1,hash.detected, cell_format)
        ws.write(row,col+2,hash.md5, cell_format)
        ws.write(row,col+3,hash.report.name, cell_format)
        ws.write(row,col+4,hash.report.creation_datetime, cell_format)
        row += 1
    
     # Adjustment of column width
    if longest_hash_len <= 32: #md5
        ws.set_column(0, 0, MD5_WIDTH)
    elif longest_hash_len <= 40: #sha1
        ws.set_column(0, 0, SHA1_WIDTH)
    else:
        ws.set_column(0, 0, SHA256_WIDTH)
    ws.set_column(2, 2, MD5_WIDTH)
    wb.close()

    return report_full_path
