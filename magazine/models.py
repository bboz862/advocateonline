import os
import datetime

from django.db import models
from django.utils.text import slugify
from django.utils.encoding import smart_unicode, smart_str
from tinymce import models as tinymce_models


def now():
    now = int((datetime.datetime.utcnow() -
                datetime.datetime(2014, 1, 1)).total_seconds() * 10 ** 6)
    return unicode(now)

# upload issue cover images
# issue_covers/issue.year/filename.jpg
def issue_upload_to(instance, filename):
    fname = ''.join([c for c in filename if c.isalnum() or c == '.'])
    return os.path.join('issue_covers', str(instance.year), now() + '_' + fname)

# upload artwork and illustrations accompanying articles
def upload_image_to(instance, filename):
    fname = ''.join([c for c in filename if c.isalnum() or c == '.'])
    print instance.issue.name
    return os.path.join('sites', 'default', 'files', fname)
    #return os.path.join('images', str(instance.issue.year), str(instance.issue.issue), now() + '_' + fname)

class Issue(models.Model):
    name = models.CharField(max_length=255, unique=True)
    theme = models.CharField(max_length=255, blank=True, null=True)
    cover_image = models.ImageField(upload_to=issue_upload_to, blank=True, null=True)

    ISSUE_CHOICES = (
        ('Fall', 'Fall'),
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Commencement', 'Commencement'),
    )
    issue = models.CharField(max_length=255, choices=ISSUE_CHOICES, default='Fall')
    year = models.IntegerField(blank=True, null=True)
    pub_date = models.DateField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/issue/{0}-{1}/'.format(self.issue.lower(), self.year)

class Section(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name

class Contributor(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
      return self.name
    def slug(self):
      return self.name.replace(" ", "_")
    def get_absolute_url(self):
     # Can't use .format because name is not always
     return '/contributor/' +  str(self.id) + '/' +  self.slug()
     # return '/contributor/{0}/{1}'.format(self.id, self.slug())



class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)

    def __unicode__(self):
        return self.name


class Content(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=100)
    teaser = models.TextField(blank=True)
    body = tinymce_models.HTMLField()

    # Legacy fields; we should probably get rid of this eventually
    medium = tinymce_models.HTMLField(blank=True)
    size = tinymce_models.HTMLField(blank=True)
    statement = tinymce_models.HTMLField(blank=True)

    issue = models.ForeignKey('Issue')
    section = models.ForeignKey('Section')
    contributors = models.ManyToManyField(Contributor)
    tags = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/content/{0}/'.format(self.id)

class Article(Content):
    photo = models.ImageField(upload_to=upload_image_to, blank=True, null=True)
    def get_absolute_url(self):
        return '/article/{0}/'.format(self.slug.lower())

class Image(Content):
    photo = models.ImageField(upload_to=upload_image_to)

class Donation(models.Model):

    amount = models.IntegerField()
    comment = models.TextField(blank=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    streetAddress1 = models.CharField(max_length=255)
    streetAddress2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    customerID = models.CharField(max_length=255)
    time = models.CharField(max_length=255)


class Subscriber(models.Model):

    SUBSCRIPTION_CHOICES = (
        ('Three year; US', 'Three year; US'),
        ('Two year; US', 'Two year; US'),
        ('One year; US', 'One year; US'),
        ('Three year; non-US', 'Three year; non-US'),
        ('Two year; non-US', 'Two year; non-US'),
        ('One year; non-US', 'One year; non-US')
    )

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    streetAddress1 = models.CharField(max_length=255)
    streetAddress2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    customerID = models.CharField(max_length=255)
    renew = models.BooleanField()
    subscriptionType = models.CharField(max_length=255, choices=SUBSCRIPTION_CHOICES)
    time = models.CharField(max_length=255)

class Purchase(models.Model):

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    streetAddress1 = models.CharField(max_length=255)
    streetAddress2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)    
    state = models.CharField(max_length=255)    
    country = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    customerID = models.CharField(max_length=255) 
    amount = models.IntegerField()
    purchases_json = models.CharField(max_length=255)
    time = models.CharField(max_length=255)

