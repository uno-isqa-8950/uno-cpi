from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from .blocks import BaseStreamBlock

class StandardPage(Page):

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )

    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
        ImageChooserPanel('image'),
    ]


class HomePage(Page):
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Homepage Hero Image'
    )

    hero_text = models.CharField(
        max_length=255,
        help_text='Write Hero Text Here',
        default='default'
        )

    body = StreamField(
        BaseStreamBlock(), verbose_name="Home content block", blank=True
    )

    promo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Promo image'
    )
    promo_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )
    promo_text = RichTextField(
        null=True,
        blank=True,
        help_text='Write some promotional copy'
    )

    featured_section_1_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )
    featured_section_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='First featured section for the homepage. Will display up to '
        'three child items.',
        verbose_name='Featured section 1'
    )

    featured_section_2_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )
    featured_section_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Second featured section for the homepage. Will display up to '
        'three child items.',
        verbose_name='Featured section 2'
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('image'),
            FieldPanel('hero_text', classname="full")],
            heading="Hero section"),
        MultiFieldPanel([
            ImageChooserPanel('promo_image'),
            FieldPanel('promo_title'),
            FieldPanel('promo_text'),
        ], heading="Promo section"),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel('featured_section_1_title'),
                PageChooserPanel('featured_section_1'),
                ]),
            MultiFieldPanel([
                FieldPanel('featured_section_2_title'),
                PageChooserPanel('featured_section_2'),
                ])
        ], heading="Featured homepage sections", classname="collapsible")
    ]

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "homepage"

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_campuspartner', False)
        extra_fields.setdefault('is_communitypartner', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def create_campuspartner(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_campuspartner') is not True:
            raise ValueError('Campus Partner must have is_campuspartner=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    is_campuspartner = models.BooleanField(default=False)
    is_communitypartner = models.BooleanField(default=False)
    avatar = models.ImageField(default='profile_image/default.jpg', upload_to='profile_image', null=True, blank=True)
    username = None
    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Contact(models.Model):
    contacttype_choices = (
        ('Primary', 'Primary'),
        ('Secondary', 'Secondary'),
        ('Other' ,'Other')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    work_phone= models.CharField(max_length=14)
    cell_phone= models.CharField(blank=True,null= True, max_length=14)
    email_id = models.EmailField(unique=False)
    contact_type = models.CharField(max_length=15, choices=contacttype_choices, default='Select')
    community_partner = models.ForeignKey('partners.CommunityPartner', on_delete=models.CASCADE,null=True,blank=True)
    campus_partner = models.ForeignKey('partners.CampusPartner', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.email_id)

    def __str__(self):
        return '%s %s ' % (self.first_name, self.last_name)


class MissionArea (models.Model):
    mission_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.mission_name)


class HouseholdIncome(models.Model):
    id2 = models.IntegerField(null=False, blank=False)
    county = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    median_income = models.IntegerField(null=False, blank=False)
    margin_error = models.IntegerField(null=False, blank=False)
    rank = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.county)
