import stripe

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.template.loader import get_template 
from django.core.mail import EmailMessage
from django.template import Context
from django.core.mail import mail_admins
from django.contrib import messages
from django.conf import settings

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from collection.forms import ThingForm, ContactForm, ThingUploadForm, EditEmailForm

from collection.models import Thing, Upload
from collection.serializers import ThingSerializer

stripe.api_key = settings.STRIPE_SECRET

def index(request):
    things = Thing.objects.all()


    # uncomment below to test the mail_admins feature!
    # mail_admins("Our subject line", "Our content")
    
    # uncomment below to test sessions!
#    request.session["thing"] = "This thing"
#    thing = request.session["thing"]
#    print (thing)

    return render(request, 'index.html', {
        'things': things,
    })


def thing_detail(request, slug):
    thing = Thing.objects.get(slug=slug)
    social_accounts = thing.social_accounts.all()

    # new: grab all the object's images
    uploads = thing.uploads.all()

    # and pass to the template
    return render(request, 'things/thing_detail.html', {
        'thing': thing,
        'social_accounts': social_accounts,
        'uploads': uploads, # don't forget to add me
    })


@login_required
def edit_thing(request, slug):
    # grab the object...
    thing = Thing.objects.get(slug=slug)

    # grab the current logged in user and make sure they're the owner of the thing
    if thing.user != request.user:
        raise Http404

    # set the form we're using...
    form_class = ThingForm

    # if we're coming to this view from a submitted form,  
    if request.method == 'POST':
        # grab the data from the submitted form
        form = form_class(data=request.POST, instance=thing)

        if form.is_valid():
            # save the new data
            form.save()

            # our new message!
            messages.success(request, 'Thing details updated.')
            return redirect('thing_detail', slug=thing.slug)

    # otherwise just create the form
    else:
        form = form_class(instance=thing)

    # and render the template
    return render(request, 'things/edit_thing.html', {
        'thing': thing,
        'form': form,
        # our publishable key!
        'key': settings.STRIPE_PUBLISHABLE,
    })


def create_thing(request):
    form_class = ThingForm

    # if we're coming from a submitted form, do this
    if request.method == 'POST':
        # grab the data from the submitted form and apply to the form
        form = form_class(request.POST)

        if form.is_valid():
            # create an instance but do not save yet
            thing = form.save(commit=False)

            # set the additional details
            thing.user = request.user
            thing.slug = slugify(thing.name)

            # save the object
            thing.save()

            # redirect to our newly created thing
            return redirect('thing_detail', slug=thing.slug)

    # otherwise just create the form
    else:
        form = form_class()

    return render(request, 'things/create_thing.html', {
        'form': form,
    })


def browse_by_name(request, initial=None):
    if initial:
        things = Thing.objects.filter(
             name__istartswith=initial).order_by('name')
    else:
        things = Thing.objects.all().order_by('name')

    return render(request, 'search/search.html', {
        'things': things,
        'initial': initial,
    })


def contact(request): 
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = form.cleaned_data['contact_name'] 
            contact_email = form.cleaned_data['contact_email'] 
            form_content = form.cleaned_data['content']

            # email the profile with the contact info 
            template = get_template('contact_template.txt')

            context = Context({ 
                'contact_name': contact_name, 
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                'New contact form submission',
                content,
                'Your website <hi@weddinglovely.com>',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('contact')

    return render(request, 'contact.html', { 
        'form': form_class,
    })


# add to the bottom
@login_required
def edit_thing_uploads(request, slug):
    # grab the object...
    thing = Thing.objects.get(slug=slug)

    # double checking just for security
    if thing.user != request.user:
        raise Http404

    # set the form we're using...
    form_class = ThingUploadForm

    # if we're coming to this view from a submitted form,
    if request.method == 'POST':
        # grab the data from the submitted form,
        # note the new "files" part
        form = form_class(data=request.POST, files=request.FILES, instance=thing)

        if form.is_valid():
            # create a new object from the submitted form
            Upload.objects.create(
                image=form.cleaned_data['image'],
                thing=thing,
            )

            return redirect('edit_thing_uploads', slug=thing.slug)

    # otherwise just create the form
    else:
        form = form_class(instance=thing)

    # grab all the object's images
    uploads = thing.uploads.all()

    # and render the template
    return render(request, 'things/edit_thing_uploads.html', {
        'thing': thing,
        'form': form,
        'uploads': uploads,
    })


@login_required
def delete_upload(request, id):
    # grab the image
    upload = Upload.objects.get(id=id)

    # security check
    if upload.thing.user != request.user:
        raise Http404

    # delete the image
    upload.delete()

    # refresh the edit page
    return redirect('edit_thing_uploads', slug=upload.thing.slug)

# our new view
@login_required
def edit_email(request, slug):
    user = request.user
    form_class = EditEmailForm

    if request.method == 'POST':
        form = form_class(data=request.POST, instance=user) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Email address updated.')
            return redirect('thing_detail', slug=slug)

    else:
        form = form_class(instance=user)

    return render(request, 'things/edit_email.html', {
        'form': form,
    })

# our new view
@login_required
def charge(request):
    # grab the logged in user, and the object the user "owns"
    user = request.user
    thing = Thing.objects.get(user=user)

    if request.method != "POST":
        # we only want to handle POST requests here, go back
        return redirect('edit_thing', slug=thing.slug)

    # check to make sure we have the proper response
    # from Stripe
    if not 'stripeToken' in request.POST:
        # the response from Stripe doesn't have a token, abort
        messages.error(request, 'Something went wrong!')
        return redirect('edit_thing', slug=thing.slug)

    try:
        # create a Stripe customer
        customer = stripe.Customer.create(
            email=request.POST['stripeEmail'],
            source=request.POST['stripeToken'],
            # our new plan!
            plan="monthly",
        )
    except stripe.StripeError as e:
        msg = "Stripe payment error: %s" % e
        messages.error(request, msg)
        mail_admins("Error on App", msg)
        return redirect('edit_thing', slug=thing.slug)

    # set the "upgraded" field to True and save the ID
    thing.upgraded = True
    thing.stripe_id = customer.id
    thing.save()

    """ our commented out code from before, no longer needed
    # set the amount to charge, in cents
    amount = 500
    # charge the customer!
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='My one-time charge',
    )
    """

    messages.success(request, 'Upgraded your account!')
    return redirect('edit_thing', slug=thing.slug)

# add your api view
@api_view(['GET', 'POST'])
def api_thing_list(request):
    """
    List all things
    """
    if request.method == 'GET':
        things = Thing.objects.all()
        serializer = ThingSerializer(things, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ThingSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_thing_detail(request, id):
    """
    Get a specific thing
    """
    try:
        thing = Thing.objects.get(id=id)
    except Thing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ThingSerializer(thing)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ThingSerializer(thing, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        thing.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)