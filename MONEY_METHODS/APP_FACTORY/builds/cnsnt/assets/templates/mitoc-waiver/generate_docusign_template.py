#!/usr/bin/env python
"""
Use an existing DocuSign template to generate a new one, including the new PDF document.
"""

import argparse
import base64
import json
import os
from datetime import datetime


def new_template_from_old(previous_json_path, waiver_pdf_path):
    """ Update the DocuSign Template JSON with a new PDF.

    The task of updating the annotated fields (if needed) is left
    as an exercise to be performed in the DocuSign interface.
    """

    with open(previous_json_path) as template_file:
        template = json.load(template_file)
    template['lastModified'] = datetime.now().isoformat() + '0Z'

    assert len(template['documents']) == 1
    with open(waiver_pdf_path, "rb") as pdf:
        base64_pdf = base64.b64encode(pdf.read())

    template['documents'][0]['documentBase64'] = base64_pdf.decode()
    return template


def main():
    """ Generate a new template document from an existing one. """
    ymd = datetime.now().date().isoformat()
    default_out = os.path.join('docusign_templates', '{}.json'.format(ymd))

    parser = argparse.ArgumentParser()
    parser.add_argument('previous_json', help="An existing DocuSign template file")
    parser.add_argument('waiver_pdf', help="A new waiver document")
    parser.add_argument('-o', dest='output_json', help="Name of output JSON", default=default_out)
    args = parser.parse_args()

    new_template = new_template_from_old(args.previous_json, args.waiver_pdf)

    with open(args.output_json, 'w') as outfile:
        json.dump(new_template, outfile, indent=4)
        print("New template written to {}".format(outfile.name))


if __name__ == '__main__':
    main()
