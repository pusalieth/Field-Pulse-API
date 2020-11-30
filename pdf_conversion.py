#!/usr/bin/python3

import base64, sys, io
import pdfkit, PyPDF2, pdf2image

this_options = {
    'page-size': 'Legal',
    'margin-top': '0in',
    'margin-bottom': '0in',
    'margin-right': '0in',
    'margin-left': '0in',
    'dpi': '300',
    'quiet': ''
}


def convert2PDF(html_string, filename=False):
    pdf_bytes = pdfkit.from_string(html_string, filename, this_options)
    return pdf_bytes


def convert2base64(bytes_object):
    bytes_base64 = base64.b64encode(bytes_object)
    return bytes_base64.decode("utf-8")

def mergePDFs(pages, convert2string=True):
    merger = PyPDF2.PdfFileMerger()
    for page in pages:
        buffer = io.BytesIO()
        buffer.write(page)
        merger.append(PyPDF2.PdfFileReader(buffer))

    file_object = io.BytesIO()
    merger.write(file_object)
    file_object.seek(0)
    if(convert2string):
        return str(file_object.getvalue())
    else:
        return file_object.getvalue()

def pdf2IMG(pdf, path=None):
    if(path == None):
        pages = pdf2image.convert_from_bytes(pdf)
    else:
        pages = convert_from_path(path)

    imgs = []
    for page in pages:
        img_file_object = io.BytesIO()
        page.save(img_file_object, 'JPEG')
        img_file_object.seek(0)
        img_base64 = convert2base64(img_file_object.getvalue())
        imgs.append('data:image/jpeg;base64,%s' % img_base64)

    return imgs

def debug(file_path='', toFile=False):
    with open(file_path, 'r') as file:
        html_page1 = file.read()

    with open(file_path, 'r') as file:
        html_page2 = file.read()

    page1 = convert2PDF(html_page1)
    page2 = convert2PDF(html_page2)
    merged_pdf = mergePDFs([page1, page2], toFile)

    # if(toFile):
    #     with open(file_path, 'wb') as file:
    #         file.write(merged_pdf.read())

    imgs = pdf2IMG(merged_pdf)
    
    return imgs
