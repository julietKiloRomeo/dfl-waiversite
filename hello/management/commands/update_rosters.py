# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 12:55:19 2015

@author: jkr
"""

from django.core.management.base import BaseCommand
from hello.util import update_league


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_league()
        self.stdout.write('League has been updated')

