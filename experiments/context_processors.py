
def web_experiments(request):
    cleaver = request.environ['cleaver']

    experiments = {}

    experiments['dashboard_background_color_experiment'] = cleaver(
        'dashboard_background_color',
        ('white', '#FFFFFF'),
        ('grey', '#F3F3F3')
    )

    if request.path == '/patients/workspace/':
        cleaver.score('dashboard_background_color')

    experiments['dashboard_title_experiment'] = cleaver(
        'dashboard_title',
        ('RapidSMS 1000 Days', 'RapidSMS 1000 Days'),
        ('1000 Days', '1000 Days'),
        ('Thousand Days', 'Thousand Days')
    )

    if request.path == '/patients/workspace/':
        cleaver.score('dashboard_title')

    return experiments
