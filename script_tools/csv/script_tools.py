# coding: utf-8

from odoo import models, _
from odoo.exceptions import UserError


class ScriptTools(models.TransientModel):
    _inherit = 'script.tools'

    def record_to_csv(self, record_ids, fields, header, split=';', line_split='\n', coding='utf-8'):
        csv = []
        for record_id in record_ids:
            record_csv = []
            for field in fields:
                value = record_id
                if type(field) is str:
                    for subfield in field.split('.'):
                        value = getattr(value, subfield)
                else:
                    value = field(record_id)
                record_csv.append(str(value))
            csv.append(split.join(record_csv))
        return line_split.join([split.join(header), line_split.join(csv)]).encode(coding)

    def read_csv(self, csv, head_from_first_line=True, header=[], split=';', line_split='\n'):
        lines = csv.split(line_split)
        if head_from_first_line:
            header = lines[0].split(split)
            lines = lines[1:]

        if not header:
            raise UserError(_('No header provided, please set a header or head_from_first_line as True.'))

        result = []
        for line in lines:
            line_datas = dict()
            i = 0
            line_content = line.split(split)
            for head in header:
                line_datas[head] = None
                if len(line_content) > i:
                    line_datas[head] = line_content[i]
                i += 1
            result.append(line_datas)

        return result
