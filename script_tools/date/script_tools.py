# coding: utf-8

from odoo import models
from odoo.fields import Date, Datetime

from dateutil.relativedelta import relativedelta
from datetime import datetime
from dateutil import tz as timezone

import logging
log = logging.getLogger().info


class ScriptTools(models.TransientModel):
    _inherit = 'script.tools'

    def auto_convert_datetime_to_tz(self, date, tz=False):
        date = Datetime.from_string(date)
        tz = tz or self.env.user.tz
        from_zone = timezone.gettz('UTC')
        date.replace(tzinfo=from_zone)

        to_zone = timezone.gettz(tz)
        return date.astimezone(to_zone)

    def date_delta(self, date, delta, delta_type='days'):
        # delta_type is one of days or months.
        d = relativedelta(days=delta)
        if delta_type == 'months':
            d = relativedelta(months=delta)
        return d + self.str_to_datetime(date)

    def format_date(self, date, format='%Y-%m-%d'):
        if type(date) is str:
            date = self.str_to_datetime(date)
        return date.strftime(format)

    def format_date_hms(self, date, format='%Y-%m-%d %H:%M:%S'):
        if type(date) is str:
            date = self.str_to_datetime(date)
        return date.strftime(format)

    def get_date_month_start_stop(self, date):
        date = self.str_to_datetime(date)
        start = self.date_delta(date, -date.day + 1, 'days')
        stop = self.date_delta(self.str_to_datetime(start), 1, 'months')
        stop = self.date_delta(stop, -1, 'days')
        return {
            'start': self.format_date(start),
            'stop': self.format_date(stop),
        }

    def get_nex_month_stop(self, date):
        date = self.str_to_datetime(date)
        start = self.date_delta(date, -date.day + 1, 'days')
        stop = self.date_delta(self.str_to_datetime(start), 1, 'months')
        stop = self.date_delta(stop, -1, 'days').replace(hour=19,minute=30,second=0)
        return {
            'stop': self.format_date_hms(stop),
        }

    def str_to_datetime(self, date_str):
        if type(date_str) is not str:
            return date_str
        if len(date_str) > 10:  # Format YYYY-mm-dd HH:MM:ss
            return Datetime.to_datetime(date_str)
        return Date.to_date(date_str)
