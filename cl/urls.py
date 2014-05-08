from django.conf.urls import patterns, include, url
from cl.recipes.views import show_recipes, show_recipes_type, show_recipe
from cl.views import show_welcome, show_welcome2, contact, contact_thanks, rcp
from cl.menus.views import show_menus, show_menus_other, show_shopping_list, show_meal, show_lateplates, add_lateplate
from cl.schedules.views import show_cleaning, show_events
from cl import mit
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

# Uncomment this for admin:
from django.contrib import admin

admin.autodiscover()
admin.site.login = login_required(admin.site.login)

urlpatterns = patterns('',
                       # Example:
                      url(r'^$', show_welcome, name='show_welcome',),
                      url(r'^recipes/$', show_recipes, name='show_recipes'),
                      url(r'^recipes/(?P<urlRecType>\d+)/$', show_recipes_type, name='show_recipes_type'),
                      url(r'^recipes/(?P<urlRecType>\d+)/(?P<urlRecId>\d+)/$',
                       show_recipe, name='show_recipe'),
                      url(r'^menus/$', show_menus, name='show_menus'),
                      url(r'^menus/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
                       show_menus_other, name='show_menus_other'),
                      url(r'^meal/(?P<meal_id>\d+)/$', show_meal, name='show_meal'),
                      url(r'^lateplates/me/(?P<meal_id>\d+)/$', add_lateplate, name='add_lateplate'),
                      url(r'^lateplates/(?P<meal_id>\d+)/$', show_lateplates, name='show_lateplates'),
                      url(r'^shopping/(?P<menu_id>\d+)/$', show_shopping_list, name='show_shopping_list'),
                      url(r'^accounts/login/',  mit.scripts_login,  name='login', ),
                       # Uncomment this for admin docs:
                      url(r'^admin/doc/', include(
                          'django.contrib.admindocs.urls')),

                       # Uncomment this for admin:
                       url(r'^admin/', include(admin.site.urls)),
                       )
urlpatterns += staticfiles_urlpatterns()
