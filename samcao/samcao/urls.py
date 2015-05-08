from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('samcao.views',
    # url(r'^time/$','current_datetime'),
    # url(r'^boots/$','boots'),
    # url(r'^time/plus/(\d{1,2})/$','hours_ahead'),
    # Examples:
    # url(r'^$', 'samcao.views.home', name='home'),
    # url(r'^samcao/', include('samcao.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('samcao.problem.views',
    url(r'^$','index'),
    url(r'^add_way/$','add_way'),
    url(r'^jy_list/$','jy_list'),
    url(r'^system_gl/$','system_gl'),
    url(r'^test_gl/$','test_gl'),
    url(r'^search/$','search'),
    url(r'^qy_email/$','qy_email'),
    url(r'^qy_emailtest/$','qy_emailtest'),
    url(r'^chinese_rules/$','chinese_rules'),
    url(r'^testtxt/$','testtxt'),
    url(r'^testb/$','testb'),
    url(r'^webmail/$','webmail'),

)


urlpatterns += patterns('',
    (r'^bootstrap/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT,}),
)