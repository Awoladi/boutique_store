from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100)
    site_description = models.TextField()
    site_logo = models.ImageField(upload_to='site_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.site_name
