from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dddd.views.home', name='home'),
    # url(r'^dddd/', include('dddd.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^$', 'views.base', name='base'),
    url(r'^myphotos', 'views.myphotos', name='myphotos'),
    #url(r'^getPhotosJson', 'views.getPhotosJson', name='getPhotosJson'),
    
    url(r'^logout$', 'views.LogoutRequest', name='LogoutRequest'),
    url(r'', include('social_auth.urls')),
    #url(r'^$', 'views.mainPage'),
    
    url('^moreImages', 'views.moreImages', name='moreImages'),
    url(r'^changeImage', 'views.changeImage', name='changeImage'),
     
    #url(r'^login/$', redirect_to, {'url': '/login/facebook'}),
    #url(r'^private', 'views.somePrivateMethod', name='someMethod'),
    #url(r'^abc$', 'views.somePrivateMethod', name='someMethod'),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
)
