# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 09:45:12 2015

@author: jkr
"""

from django.core.management.base import BaseCommand
from hello.util import clear_all_bids


class Command(BaseCommand):
    def handle(self, *args, **options):
        clear_all_bids()
        self.stdout.write('All bids have been deleted')

