
import hashlib

from .models import AuditTrail
from django.core import serializers


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def store_audit(*, request, instance, action, previous_instance=None):
	audit = AuditTrail()
	audit.model_type = instance._meta.verbose_name.title()
	audit.object_id = instance.pk
	audit.object_str = str(instance)
	audit.action = action
	audit.user = request.user
	audit.ip = get_client_ip(request)
	audit.instance = serializers.serialize("json", [instance])
	if previous_instance:
		audit.previous_instance = serializers.serialize("json", [previous_instance])
	audit.save()




import re

from random import randint

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .encryption import _encrypt, _decrypt, _isEncrypted
from .models import User


class OTPEncryptionDec():
	def _encrypt_otp(self):
		rand_otp = randint(100000, 999999)
		encrypted_otp = _encrypt(str(rand_otp))
		return {"otp":rand_otp, "encrypted_otp":encrypted_otp}

	def _decrypt_otp(self, encrypted_otp):
		if _isEncrypted(encrypted_otp):
			dec_otp = _decrypt(encrypted_otp)
			return dec_otp
		return encrypted_otp
	
	def _decrypt_validate_otp(self, encrypted_otp, otp):
		if _isEncrypted(encrypted_otp):
			dec_otp = _decrypt(encrypted_otp)
			if dec_otp == otp:
				return True
		return False
	

class TokenEncodeDecode():

	def _encode(self, user):

		token = default_token_generator.make_token(user)
		uid = urlsafe_base64_encode(bytes(str(user.uuid), 'utf-8'))
		return {"token": token, "uid": uid}
	
	def _decode(self,uid, token):
		
		try:
			uid = urlsafe_base64_decode(uid)
			uid = uid.decode('utf-8')  # Decode bytes to str using utf-8
			user = User.objects.get(uuid=uid)
			if default_token_generator.check_token(user, token):
				return {"user": user}
		except:
			return False

from django.core import serializers
from django.conf import settings
from django.core.cache.backends.base import  DEFAULT_TIMEOUT
from django.core.exceptions import PermissionDenied
from django.conf import settings

import redis


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
RATE_LIMIT_DURATION = settings.RATE_LIMIT_DURATION
MAX_REQUESTS_PER_MINUTE = 5

import time

redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)



def generate_token(request):

	ip_address = request.META.get('REMOTE_ADDR')
	user_agent = request.META.get('HTTP_USER_AGENT')
	payload = {'ip_address': ip_address}
	token = hashlib.sha256((str(payload) + user_agent).encode()).hexdigest()
	return token



def rate_limit(request):

	token = request.session.get('rate_limit_token')
	if not token:
		token = generate_token(request)
		request.session['rate_limit_token'] = token

	current_count = int(redis_conn.get(token) or 0)
	last_request_time = int(redis_conn.get(token + '_time') or 0)
	current_time = int(time.time())

	# Calculate the time elapsed since the last request
	time_elapsed = current_time - last_request_time if last_request_time else 0

	# Reset the count if the time window has expired
	if time_elapsed >= RATE_LIMIT_DURATION:
		current_count = 0

	print(current_count)
	# Check if the user has exceeded the rate limit
	if current_count >= MAX_REQUESTS_PER_MINUTE:
		raise PermissionDenied

	# Update the count and timestamp in Redis
	redis_conn.set(token, current_count + 1, ex=RATE_LIMIT_DURATION)
	redis_conn.set(token + '_time', current_time, ex=RATE_LIMIT_DURATION)