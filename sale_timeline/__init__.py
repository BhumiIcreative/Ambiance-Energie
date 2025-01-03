from . import models


def _pre_init_hook(env):
    term_id = env['account.payment.term'].search([('name','=','Payment timeline')])
    if not term_id:
        term_id = env['account.payment.term'].create({'name':'Payment timeline'})
        ir_model_id = env['ir.model.data'].create({'name':'timeline_payment',
                                               'model':'account.payment.term',
                                               'res_id':term_id.id,
                                               'noupdate': True,
                                               'module':'sale_timeline'})
