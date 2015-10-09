from django.conf import settings
import util

def custom(request):
    u               = request.user
    lock_bids       = settings.LOCK_BIDS or (not util.is_1_waiver_period())
    has_permission  = u.is_staff or u.is_superuser
    return {'lock_bids':lock_bids, 'has_permission':has_permission}    
    