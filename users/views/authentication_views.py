import random
import string

import requests
from django.conf import settings
from django.contrib.auth import login as django_login
from django.http import HttpResponse
from django.shortcuts import redirect, render, reverse
from django.views import View

from users.models import CustomUser

state = None


def login(request):
    global state
    state = generate_random_state()
    url = f'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={settings.LINKEDIN_CLIENT_ID}&redirect_uri={settings.LINKEDIN_CALLBACK_URL}&state={state}&scope=openid,profile,email,w_member_social,r_basicprofile'
    return render(request, 'login.html', {'url': url})


def generate_random_state():
    characters = string.ascii_letters + string.digits
    random_state = ''.join(random.choice(characters) for _ in (range(100)))
    return random_state


def logout(request):
    request.session.clear()
    return redirect(reverse('home'))


def index(request):
    return redirect('login')


def home(request):
    return render(request, 'home.html')


class LinkedInCallbackView(View):
    def get(self, request):
        code = request.GET.get('code')
        state_get = request.GET.get('state')
        if state_get != state:
            return HttpResponse('Unauthorized', status=401)

        response = self.response_data(code)

        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token')
            user_data = self.fetch_userinfo(access_token)
            profile_data = self.fetch_profile_data(access_token)
            user_data['profile_link'] = f'https://www.linkedin.com/in/{profile_data["vanityName"]}/'
            user = self.create_or_get_user(user_data, profile_data, access_token, refresh_token)
            django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return render(request, 'success.html',
                          {'access_token': access_token, 'refresh_token': refresh_token, 'user_data': user_data})
            # return redirect('home')
        else:
            return HttpResponse('Failed to obtain access token', status=400)

    @staticmethod
    def response_data(code):
        token_params = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': settings.LINKEDIN_CLIENT_ID,
            'client_secret': settings.LINKEDIN_CLIENT_SECRET,
            'redirect_uri': settings.LINKEDIN_CALLBACK_URL,
        }

        response = requests.post('https://www.linkedin.com/oauth/v2/accessToken', data=token_params,
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'})
        return response

    @staticmethod
    def fetch_userinfo(access_token):
        profile_url = 'https://api.linkedin.com/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(profile_url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return user_data
        return None

    @staticmethod
    def fetch_profile_data(access_token):
        profile_url = 'https://api.linkedin.com/v2/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(profile_url, headers=headers)
        if response.status_code == 200:
            profile_data = response.json()
            return profile_data
        return None

    @staticmethod
    def create_or_get_user(user_data, profile_data, access_token, refresh_token):
        linkedin_id = user_data.get('sub')
        email = user_data.get('email')
        full_name = user_data.get('name')
        picture = user_data.get('picture')
        profile_link = f'https://www.linkedin.com/in/{profile_data["vanityName"]}/'

        try:
            user = CustomUser.objects.get(email=email)
            user.linkedin_id = linkedin_id
            user.access_token = access_token
            user.refresh_token = refresh_token
            user.full_name = full_name
            user.picture = picture
            user.profile_link = profile_link
            user.save()
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(
                linkedin_id=linkedin_id,
                email=email,
                access_token=access_token,
                refresh_token=refresh_token,
                full_name=full_name,
                picture=picture,
                profile_link=profile_link
            )

        return user
