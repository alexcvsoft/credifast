from django.contrib import admin

from .models import Application
from .models import AddressProof
from .models import Decision
from .models import RuleLog


admin.site.register(Application)
admin.site.register(AddressProof)
admin.site.register(Decision)
admin.site.register(RuleLog)