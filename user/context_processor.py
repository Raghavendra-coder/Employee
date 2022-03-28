from .models import Leaves


def global_values(request):
    request_count = Leaves.objects.filter(status='P').count()

    context = {
        'request_count': request_count,
    }

    return context
