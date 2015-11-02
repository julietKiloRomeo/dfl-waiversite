from django.conf import settings
import util
from django.utils import timezone

def custom(request):
    u               = request.user
    lock_bids       = settings.LOCK_BIDS or (not util.is_1_waiver_period())
    has_permission  = u.is_staff or u.is_superuser
    ms_left         = util.time_until_open().seconds*1000 + util.time_until_open().days*24*60*60*1000
    now             = timezone.localtime(timezone.now())
    if util.is_1_waiver_period():
        waiver_period   = 1
    else:
        waiver_period   = 2
        
    return {'lock_bids':lock_bids, 
            'has_permission':has_permission, 
            'waiver_period':waiver_period,
            'now':now,
            'ms_left':ms_left}    
    