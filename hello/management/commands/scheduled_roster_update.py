# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 10:58:40 2015

@author: jkr
"""

from django.core.management.base import BaseCommand
from hello.util import update_league
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        current_time = datetime.datetime.now()
        is_wednesday_or_tuesday = current_time.weekday() == 2 or current_time.weekday() == 1

        if is_wednesday_or_tuesday:
            update_league()
            self.stdout.write('League has been updated')
        else:
            self.stdout.write('Not wednesday. No update. See you tomorrow.')
