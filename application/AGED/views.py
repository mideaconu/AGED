# 
# AGED/views.py
#
# Author: Mihai Ionut Deaconu
#

import os
from django.conf import settings
from django.http import HttpResponse, Http404

def download(request, pk, name):
  file_path = os.path.join(settings.MEDIA_ROOT, "count_data", pk, name)
  if os.path.exists(file_path):
    with open(file_path, 'rb') as fh:
      response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
      response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
      return response
  raise Http404