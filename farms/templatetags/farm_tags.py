from django import template

register = template.Library()

CHANNEL_LABELS = {
    'farm_gate': 'Farm Gate',
    'u_pick': 'U-Pick',
    'delivery': 'Delivery',
    'farmers_market': "Farmers' Market",
    'online': 'Online Store',
    'csa': 'CSA Box',
}

CERT_LABELS = {
    'organic': 'Certified Organic',
    'grass_fed': 'Grass Fed',
    'free_range': 'Free Range',
    'pasture_raised': 'Pasture Raised',
    'no_spray': 'No Spray',
    'non_gmo': 'Non-GMO',
}


@register.filter
def channel_label(value):
    return CHANNEL_LABELS.get(value, value.replace('_', ' ').title())


@register.filter
def cert_label(value):
    return CERT_LABELS.get(value, value.replace('_', ' ').title())
