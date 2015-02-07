from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('samcao.views',
    url(r'^$','hello'),
    url(r'^time/$','current_datetime'),
    url(r'^boots/$','boots'),
    # Examples:
    # url(r'^$', 'samcao.views.home', name='home'),
    # url(r'^samcao/', include('samcao.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
# urlpatterns += patterns('',
#     (r'^bootstrap/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
# )
# urlpatterns += patterns('',
#     url(r'^staticfiles/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATICFILES_DIRS, 'show_indexes': True}),
# )