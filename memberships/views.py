from rest_framework.decorators import api_view, permission_classes, APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import MembershipSerializer, UserMembershipSerializer, SubscriptionSerializer
from .models import Membership, UserMembership, Subscription
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.urls import reverse



def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None

def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None

def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
        membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)

    user_membership_serializer = UserMembershipSerializer(user_membership)
    user_subscription_serializer = SubscriptionSerializer(user_subscription)

    return Response({
        'user_membership': user_membership_serializer.data,
        'user_subscription': user_subscription_serializer.data
    })

class MembershipSelectView(APIView):
    def get(self, request):
        memberships = Membership.objects.all()
        serializer = MembershipSerializer(memberships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)
        selected_membership_type = request.data.get('membership_type')

        selected_membership = get_object_or_404(Membership, membership_type=selected_membership_type)

        if user_membership.membership == selected_membership:
            if user_subscription is not None:
                # Return an appropriate response, such as a JSON message
                return Response({'message': 'You already have this membership. Your next payment is due.'}, status=status.HTTP_400_BAD_REQUEST)

        # Assign to the session
        request.session['selected_membership_type'] = selected_membership.membership_type

        # Redirect to the payment endpoint on your React frontend
        return Response({'redirect_url': reverse('memberships:payment')}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment_view(request):
    user_membership = get_user_membership(request)

    try:
        selected_membership_type = request.data.get('membership_type')
        selected_membership = Membership.objects.get(membership_type=selected_membership_type)

        if user_membership.membership == selected_membership:
            user_subscription = get_user_subscription(request)
            if user_subscription is not None:
                return Response({
                    'message': f'You already have this membership. Your next payment is due {user_subscription.next_payment_date}'  # Update with actual next payment date
                })

        request.session['selected_membership_type'] = selected_membership.membership_type

        return Response({
            'message': 'Membership type selected successfully',
            'selected_membership': MembershipSerializer(selected_membership).data
        })
    except Membership.DoesNotExist:
        return Response({'error': 'Selected membership type not found'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_transaction_records(request, subscription_id):
    user_membership = get_user_membership(request)

    try:
        selected_membership = Membership.objects.get(membership_type=request.session.get('selected_membership_type'))

        user_membership.membership = selected_membership
        user_membership.save()

        sub, created = Subscription.objects.get_or_create(user_membership=user_membership)
        sub.stripe_subscription_id = subscription_id
        sub.active = True
        sub.save()

        del request.session['selected_membership_type']

        return Response({
            'message': f'Successfully created {selected_membership} membership'
        })
    except Membership.DoesNotExist:
        return Response({'error': 'Selected membership type not found'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_subscription(request):
    user_sub = get_user_subscription(request)

    if user_sub.active is False:
        return Response({'message': 'You dont have an active membership'})

    # Use Stripe API to cancel the subscription here

    user_sub.active = False
    user_sub.save()

    free_membership = Membership.objects.get(membership_type='Free')
    user_membership = get_user_membership(request)
    user_membership.membership = free_membership
    user_membership.save()

    # Send an email here

    return Response({'message': 'Successfully cancelled membership'})