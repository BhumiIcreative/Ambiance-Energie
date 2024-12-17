# coding: utf-8

from odoo import models, api, _
from odoo.fields import *

from collections import OrderedDict

import logging
log = logging.getLogger().info


EXCLUDED_FIELDS = [
    'id', 'create_date', 'create_uid', 'write_date', 'write_uid', '__last_update'
]


class ExportRecordToXml(models.TransientModel):
    _name = 'script.export.record.xml'
    _description = _('Export record to xml')

    def _get_reference_selection(self):
        return [
            (x.model, '[%s] %s' % (x.model, x.name))
            for x in self.env['ir.model'].search([], order='model')
        ]

    record_id = Reference(_get_reference_selection, required=True, string=_('Record to export'))
    xml_id = Char(_('XML id'), compute='_cpt_xml_id', store=True)

    field_ids = Many2many('ir.model.fields', string=_('Exported fields'), compute='_cpt_field_ids', store=True)

    @api.depends('record_id')
    def _cpt_xml_id(self):
        for wiz_id in self:
            wiz_id.xml_id = ''
            if wiz_id.record_id:
                wiz_id.xml_id = '%s_%s' % (wiz_id.record_id._name.replace('.', '_'), wiz_id.record_id.id)

    @api.depends('record_id')
    def _cpt_field_ids(self):
        for wiz_id in self:
            if not wiz_id.record_id:
                continue
            model_id = self.env['ir.model'].search([
                ('model', '=', wiz_id.record_id._name),
            ])
            field_ids = model_id.field_id
            field_ids = field_ids.filtered(lambda x: x.name not in EXCLUDED_FIELDS)
            field_ids = field_ids.filtered(lambda x: not x.compute)

            field_ids_to_export = self.env['ir.model.fields']
            for field_id in field_ids:
                if getattr(wiz_id.record_id, field_id.name) or field_id.ttype == 'boolean':
                    field_ids_to_export |= field_id
            wiz_id.field_ids = [(6, 0, field_ids_to_export.ids)]

    def find_external_id(self, record_id):
        IrModelData = self.env['ir.model.data']
        if not record_id:
            return IrModelData
        return IrModelData.search([
            ('model', '=', record_id._name),
            ('res_id', '=', record_id.id),
        ], limit=1)

    def export(self):
        Script = self.env['script.tools']
        res = []
        for field_id in self.field_ids:
            if field_id.ttype in ['many2one']:
                res.append(self.export_many2one(field_id))
            elif field_id.ttype in ['reference']:
                res.append(self.export_reference(field_id))
            elif field_id.ttype in ['one2many', 'many2many']:
                res.append(self.export_x2many(field_id))
            elif field_id.ttype in ['html']:
                res.append(self.export_html(field_id))
            else:
                value = getattr(self.record_id, field_id.name)
                if value and type(value) is str:
                    value = value.replace('<', '&lt;')
                    value = value.replace('>', '&gt;')
                    value = value.replace('&', '&amp;')
                    value = value.replace('&nbsp;', ' ')
                if value or field_id.ttype in ['boolean', 'float', 'integer', 'monetary']:
                    res.append({
                        '@name': field_id.name,
                        '': value,
                    })
        datas = {
            '@model': self.record_id._name,
            '@id': self.xml_id,
            '': [{'field': x} for x in res],
        }
        xml = Script.dict_to_xml(datas, root='record')
        log(xml)
        return Script.download_text(xml, '%s.xml' % (self.xml_id))

    def export_html(self, field_id):
        value = getattr(self.record_id, field_id.name)
        auto_close_tags = ['img', 'br', 'hr']
        for tag in auto_close_tags:
            splitted = value.split('<%s' % tag)
            res = splitted[0]
            if len(splitted) == 1:
                continue
            for e in splitted[1:]:
                e_splitted = e.split('>')
                res += e_splitted[0] + '/>'
                if len(e_splitted) > 1:
                    res += '>'.join(e_splitted[1:])
            value = res
        return {
            '@name': field_id.name,
            '@type': 'xml',
            '': value,
        }

    def export_many2one(self, field_id):
        record_id = getattr(self.record_id, field_id.name)
        external_id = self.find_external_id(record_id)
        if external_id:
            return {
                '@name': field_id.name,
                '@ref': external_id.complete_name,
            }
        return {
            '@name': field_id.name,
            '': record_id.id,
        }

    def export_reference(self, field_id):
        record_id = getattr(self.record_id, field_id.name)
        return {
            '@name': field_id.name,
            '': '%s,%s' % (record_id._name, record_id.id),
        }

    def export_x2many(self, field_id):
        record_ids = getattr(self.record_id, field_id.name)
        res = []
        for record_id in record_ids:
            external_id = self.find_external_id(record_id)
            if external_id:
                res.append("ref('" + external_id.complete_name + "')")
            else:
                res.append(str(record_id.id))
        return {
            '@name': field_id.name,
            '@eval': '[(6, 0, [' + ', '.join(res) + '])]',
        }
