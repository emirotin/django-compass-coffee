from models import *

def recent_polls(request):
    recent_polls = Poll.objects.all().order_by('-pk')[:5]
    return {'recent_polls': recent_polls}
