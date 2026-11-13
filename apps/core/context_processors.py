from apps.tours.models import Service


def site_info(request):
    return {
        'SITE': {
            'name': 'MORTEL ADVENTURES',
            'tagline': 'explore & tell more',
            'about': 'Your gateway to thrilling travel experiences, breathtaking destinations and unforgettable memories.',
            'phone1': '0791818170',
            'phone2': '0711191480',
            'email': 'morteladventures@gmail.com',
            'whatsapp': '254793079569',                  
            'address': '50504-00100',  
            'hours': 'Mon–Sat: 8:00 AM – 6:00 PM',       # EDIT
            'map_query': 'Imara Daima, Nairobi, Kenya',               # EDIT: use your office address
            'facebook': '#', 'instagram': '#', 'tiktok': '#',
        },
        'footer_services': Service.objects.filter(is_active=True)[:5],
    }