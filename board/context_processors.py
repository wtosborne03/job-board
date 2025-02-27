from django.urls import reverse


def active_tab(request):
    path = request.path

    home_urls = [reverse('home'), reverse('employer_home')]
    message_urls = [
        reverse('inbox'),
        reverse('send_message'),
        reverse('message_detail', args=['1'])[:-1]
    ]
    profile_urls = [
        reverse('profile'),
    ]
    dashboard_urls = [
        reverse('my_applications'),
    ]

    active = None
    if any(path == url for url in home_urls):
        active = 'home'
    if any(path.startswith(url) for url in message_urls):
        active = 'messages'
    if any(path.startswith(url) for url in profile_urls):
        active = 'profile'
    if any(path.startswith(url) for url in dashboard_urls):
        active = 'dashboard'

    return {'active_tab': active}
