from django.conf import settings
import util

def custom(request):
    u               = request.user
    lock_bids       = settings.LOCK_BIDS or (not util.is_1_waiver_period())
    has_permission  = u.is_staff or u.is_superuser
    waiver_period   = 2
    ms_left         = util.time_until_open().seconds*1000 + util.time_until_open().days*24*60*60*1000
    if util.is_1_waiver_period():
        waiver_period   = 1
        ms_left         = 0
    return {'lock_bids':lock_bids, 
            'has_permission':has_permission, 
            'waiver_period':waiver_period,
            'ms_left':ms_left}    
    