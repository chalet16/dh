from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from myForms import ContactForm
from django.core.mail import send_mail
from cl.menus.models import *
from cl.menus.views import *
from datetime import *
from menus.views import menu_weeks


def get_today():
    now = datetime.now().date()
    week_start = now - timedelta(now.isoweekday() % 7)
    week_end = week_start + timedelta(6)
    try:
        menu = Menu.objects.filter(date__range=(week_start, week_end))[0]
        meals = []
        mealsQ = Meal.objects.filter(menu__pk__exact=menu.pk).filter(
            crew__day__exact=now.strftime("%a"))
        for meal in mealsQ:
            meals.append(mealObj(meal))
    except:
        meals = []
    return meals


def show_welcome2(request):
    meals = get_today()
    return render_to_response('pages/welcome.html', {'meals': meals})


def rcp(request):
    meals = get_today()
    return render_to_response('pages/rcpes.html', {'meals': meals})


def show_welcome(request):
    meals = get_today()
    date = menu_weeks(datetime.now().date())
    return render_to_response('pages/index.html', {'meals': meals,'date':date})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.full_clean()
            who = form.cleaned_data['who']
            topic = form.cleaned_data['topic']
            myMessage = u'%s:\r\n%s' % (topic, form.cleaned_data['message'])
            sender = form.cleaned_data['sender']
            send_mail('Feedback from dh.xvm.mit.edu for %s' %
                      who, myMessage, sender, ['jacohen@mit.edu'])
            return HttpResponseRedirect('/cl/contact/thanks/')
    else:
        form = ContactForm()
    return render_to_response('pages/contact.html', {'form': form})


def contact_thanks(request):
    return render_to_response('pages/contact_thanks.html')
