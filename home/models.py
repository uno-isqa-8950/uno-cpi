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
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet
from simple_history.models import HistoricalRecords

class HomePage(Page):

    # Hero section of HomePage
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Homepage image'
    )
    hero_text = models.CharField(
        max_length=255,
        help_text='Write an introduction for the Site'
        )

    # Body section of the HomePage
    body = StreamField(
        BaseStreamBlock(), verbose_name="Home content block", blank=True
    )

    bottom = StreamField(
        BaseStreamBlock(), verbose_name="Home content block", blank=True
    )

    # Promo section of the HomePage
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

    featured_section_3_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )
    featured_section_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Third featured section for the homepage. Will display up to '
        'six child items.',
        verbose_name='Featured section 3'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('image'),
            FieldPanel('hero_text', classname="full"),
        ], heading="Hero section"),
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
                ]),
            MultiFieldPanel([
                FieldPanel('featured_section_3_title'),
                PageChooserPanel('featured_section_3'),
                ])
        ], heading="Featured homepage sections", classname="collapsible"),
        StreamFieldPanel('bottom')
    ]

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "homepage"

class BlogPage(Page):

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
    subtitle = models.CharField(blank=True, max_length=255)
    external_link = models.CharField(blank=True, max_length=255)


    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="full"),
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
        StreamFieldPanel('body'),
        FieldPanel('external_link', classname="full"),
    ]

    parent_page_types = ['BlogIndexPage']

    # Specifies what content types can exist as children of BlogPage.
    # Empty list means that no child content types are allowed.
    subpage_types = []


class BlogIndexPage(RoutablePageMixin, Page):

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

    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        ImageChooserPanel('image'),
    ]

    # Speficies that only BlogPage objects can live under this index page
    subpage_types = ['BlogPage']

    # Defines a method to access the children of the page (e.g. BlogPage
    # objects). On the demo site we use this on the HomePage
    def children(self):
        return self.get_children().specific().live()

    # Overrides the context to list all child items, that are live, by the
    # date that they were published
    # http://docs.wagtail.io/en/latest/getting_started/tutorial.html#overriding-context
    def get_context(self, request):
        context = super(BlogIndexPage, self).get_context(request)
        context['posts'] = BlogPage.objects.descendant_of(
            self).live().order_by(
            '-date_published')
        return context

    # This defines a Custom view that utilizes Tags. This view will return all
    # related BlogPages for a given Tag or redirect back to the BlogIndexPage.
    # More information on RoutablePages is at
    # http://docs.wagtail.io/en/latest/reference/contrib/routablepage.html
    # @route('^tags/$', name='tag_archive')
    # @route('^tags/([\w-]+)/$', name='tag_archive')
    # def tag_archive(self, request, tag=None):
    #
    #     try:
    #         tag = Tag.objects.get(slug=tag)
    #     except Tag.DoesNotExist:
    #         if tag:
    #             msg = 'There are no blog posts tagged with "{}"'.format(tag)
    #             messages.add_message(request, messages.INFO, msg)
    #         return redirect(self.url)
    #
    #     posts = self.get_posts(tag=tag)
    #     context = {
    #         'tag': tag,
    #         'posts': posts
    #     }
    #     return render(request, 'blog/blog_index_page.html', context)

    def serve_preview(self, request, mode_name):
        # Needed for previews to work
        return self.serve(request)

    # Returns the child BlogPage objects for this BlogPageIndex.
    # If a tag is used then it will filter the posts by tag.
    def get_posts(self, tag=None):
        posts = BlogPage.objects.live().descendant_of(self)
        if tag:
            posts = posts.filter(tags=tag)
        return posts

    # # Returns the list of Tags for all child posts of this BlogPage.
    # def get_child_tags(self):
    #     tags = []
    #     for post in self.get_posts():
    #         # Not tags.append() because we don't want a list of lists
    #         tags += post.get_tags
    #     tags = sorted(set(tags))
    #     return tags

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
    # history = HistoricalRecords()


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
    history = HistoricalRecords()

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
    history = HistoricalRecords()

    def __str__(self):
        return str(self.county)
class DataDefinitionGroup (models.Model):
    group = models.CharField(max_length=100,default="Default")

    def __str__(self):
        return str(self.group)

class DataDefinition(models.Model):
    id = models.IntegerField(unique=True,null=False, blank=False, primary_key=True)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)
    group = models.ForeignKey('DataDefinitionGroup', on_delete=models.CASCADE,default=True)
    is_active = models.BooleanField(default=False)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.title)

@register_snippet
class Campus_Partner_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Campus Partner Snippet"

@register_snippet
class Campus_Partner_User_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Campus Partner User Snippet"

@register_snippet
class Community_Partner_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Community Partner Snippet"

@register_snippet
class Community_Partner_User_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Community Partner User Snippet"

@register_snippet
class Public_Project_Report_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Public Project Report Snippet"

@register_snippet
class Private_Project_Report_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Private Project Report Snippet"

@register_snippet
class Community_Public_Report_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Community Public Report Snippet"

@register_snippet
class Community_Private_Report_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Community Private Report Snippet"

@register_snippet
class Engagement_Types_Report_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Engagement Types Report Snippet"

@register_snippet
class Mission_Areas_Report_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Mission Areas Report Snippet"

@register_snippet
class Mission_Areas_Chart_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Mission Areas Charts Snippet"

@register_snippet
class Engagement_Types_Chart_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Engagement Types Chart Snippet"

@register_snippet
class Register_Campus_Partner_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Register Campus Partner Snippet"

@register_snippet
class Register_Community_Partner_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Register Community Partner Search Snippet"

@register_snippet
class Register_Campus_Partner_User_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Register Campus Partner User Snippet"

@register_snippet
class Register_Community_Partner_User_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Register Community Partner User Snippet"

@register_snippet
class All_Projects_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "All Projects Page Snippet"

@register_snippet
class My_Projects_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "My Projects Page Snippet"

@register_snippet
class Create_Projects_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Create Projects Search Page Snippet"

@register_snippet
class Create_Projects_Form_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Create Projects Form Snippet"

@register_snippet
class Register_Community_Partner_Form_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Register Community Partner Form Snippet"

@register_snippet
class Community_Partner_Project_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Community Partner Project Snippet"

@register_snippet
class Partners_User_Profile_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Partners User Profile Snippet"

@register_snippet
class Partners_User_Profile_Update_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Partners User Profile Update Snippet"

@register_snippet
class Partners_Organizatiion_Profile_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Partners Organization Profile Snippet"

@register_snippet
class Partners_Organizatiion_Profile_Contacts_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Partners Organization Profile Contacts Snippet"

@register_snippet
class Partners_Organizatiion_Profile_Partners_Add_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Partners Organization Profile Partners Add Snippet"

@register_snippet
class Partners_Organizatiion_Profile_Partners_Update_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Partners Organization Profile Partners Update Snippet"

@register_snippet
class Logout_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Logout Snippet"

@register_snippet
class Login_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Login Snippet"

@register_snippet
class Password_Reset_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Password Reset Snippet"

@register_snippet
class Password_Reset_Done_Snippet(models.Model):
    text = models.CharField(max_length=1250)

    panels = [
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Password Reset Done_Snippet"