from django.core.mail import send_mail
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework.response import Response
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from bundle.models import Bundle, Paper
from .serializers import BundleSerializer
import stripe
import os


class BundleViewSet(viewsets.ModelViewSet):
    queryset = Bundle.objects.all()
    serializer_class = BundleSerializer

    # def create(self, request):
    #     serializer = self.serializer_class()
    #     data = serializer.data
    #     return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def create_checkout_session(request):
    price = request.data['price']
    quantity = 1
    domain_url = os.environ.get('DOMAIN_URL')

    try:
        # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - lets capture the payment later
        # [customer_email] - lets you prefill the email input in the form
        # [automatic_tax] - to automatically calculate sales tax, VAT and GST in the checkout page
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url +
            '/?success=true?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + '/?canceled=true',
            mode='payment',
            # automatic_tax={'enabled': True},
            payment_method_types=[
                'card'
            ],
            line_items=[{
                'price': price,
                'quantity': quantity,
            }],
            metadata={
                'price': price
            }
        )
        return Response({'checkout_url': checkout_session.url})
    except Exception as e:
        return Response({'error': str(e)}, status=403)


@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def webhook(request):
    event = None
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']

    endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return Response({'status': 'Invalid payload'})
    except stripe.error.SignatureVerificationError as e:
        return Response({'status': 'Invalid signature'})

    # Handle the event
    if event['type'] == 'price.updated':
        price = event['data']['object']
        product = Bundle.objects.get(stripe_id=price.product)
        product.price = price['unit_amount']
        product.price_id = price['id']
        product.save()
        return Response({'status': 'Product updated'})
    elif event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        checkout_session = stripe.checkout.Session.list(
            payment_intent=payment_intent['id'], expand=['data.line_items'])
        for item in checkout_session['data'][0]['line_items']['data']:
            product_id = item['price']['product']
            bundle_bought = Bundle.objects.get(stripe_id=product_id)

            send_mail(
                'Path of resources order',
                f"Thanks for shopping! Here is your link {bundle_bought.airtable_url}",
                'dimitrisstefanakis1@gmail.com',
                ['jimstef@outlook.com'],
                fail_silently=False,
            )

        return Response({'status': 'ok'})
    else:
        print('Unhandled event type {}'.format(event['type']))
        return Response({'status': 'Unhandled event type'})
