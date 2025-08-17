from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class SupabasePublicStorage(S3Boto3Storage):
    def url(self, name):
        # Build the public URL format for Supabase
        return f"{settings.SUPABASE_PUBLIC_URL}/{name}"
