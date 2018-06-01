from django.contrib import admin
from .models import Account, Event, Region, Season, EventActivity, EventType, Summary, Log, School, Team, MemberGroup, Member

admin.site.register(Account);
admin.site.register(Event);
admin.site.register(Region);
admin.site.register(Season);
admin.site.register(EventActivity);
admin.site.register(EventType);
admin.site.register(Summary);
admin.site.register(Log);
admin.site.register(School);
admin.site.register(Team);
admin.site.register(MemberGroup);
admin.site.register(Member);