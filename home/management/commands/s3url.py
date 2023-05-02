import boto3
from django.core.management.base import BaseCommand
from home.models import MissionArea
from UnoCPI.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME


# APP_ENV = os.environ.get('APP_ENV')

# function to fix S3 URLs for objects based on env
def s3UrlPicker():
    url_list = []
    name_list = []
    bucket_name = AWS_STORAGE_BUCKET_NAME
    folder_name = 'missionarea_images/'
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    missions = MissionArea.objects.all()
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    # picks image URLs for all focus areas
    for obj in objects['Contents']:
        image_url = s3.generate_presigned_url(ClientMethod='get_object',
                                              Params={'Bucket': bucket_name, 'Key': obj['Key']})
        url_parts = image_url.split('?')
        url_without_query_string = url_parts[0] if len(url_parts) > 1 else image_url
        url_list.append(url_without_query_string)

    # picks mission area names from MissionArea
    for mission in missions:
        name_list.append(mission.mission_name)

    url_map = {}

    for i in range(len(url_list)):
        url_map[name_list[i]] = url_list[i]

    # saving the url_map dictionary contents into MissionArea mission_image_url column
    for mission_area in MissionArea.objects.all():
        mission_area.mission_image_url = url_map.get(mission_area.mission_name)
        mission_area.save()


# Django custom command usage: python manage.py <command>
class Command(BaseCommand):
    def handle(self, *args, **options):
        s3UrlPicker()
