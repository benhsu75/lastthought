from django.conf.urls import url, patterns
from django.contrib import admin
from main.views import general, log_views
from main.entrypoints.messenger import messenger
from django.conf import settings

urlpatterns = [
    url(r'^$', general.index),

    # Messenger webhooks
    url(r'^messenger_callback/', messenger.messenger_callback),
    url(r'^messenger_account_link/', messenger.account_link),

    # Facebook Login
    url(r'^fblogin_view/', general.fblogin_view),
    url(r'^fblogin_redirect/', general.fblogin_redirect),

    # Account management
    url(r'^logout/', general.logout_view),
    url(r'^login/', general.login_view),
    url(r'^try/', general.try_view),
    url(r'^settings/', general.settings),

    # Log endpoints
    url(r'^logs/(?P<logentry_id>\d+)/$', log_views.logs),
    url(r'^logs/$', log_views.logs),
    url(r'^log_contexts/(?P<logcontext_id>\d+)/$', log_views.log_contexts),

    # Display endpoints
    url(r'^users/(?P<fbid>\d+)/logs', log_views.index),
    url(
        r'^categories/(?P<log_context_id>\d+)',
        log_views.log_context_show
    ),
]

# Ensure static files are accessible
if True:
    urlpatterns += patterns(
        '',
        (
            r'^static/(?P<path>.*)$',
            'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}
        ),
    )
