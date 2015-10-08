from django.conf import settings

def custom(request):
    u         = request.user
    let_me_in = settings.SHOW_RESULTS or (u.is_staff and settings.SHOW_RESULTS_FOR_STAFF) or (u.is_superuser and settings.SHOW_RESULTS_FOR_SU)
    lock_bids = settings.LOCK_BIDS
    has_permission = u.is_staff or u.is_superuser
    return {'show_results': let_me_in, 'lock_bids':lock_bids, 'has_permission':has_permission}    
    