#!/bin/bash

# Set the environment variable for the Heroku app
heroku config:set ENV_NAME=$1

# Run the Django migration to update the database schema
heroku run python manage.py migrate

# Get the AWS credentials and session for the current environment
# Will remove any extra vars that are not needed in the script after review
AWS_ACCESS_KEY_ID=$(heroku config:get AWS_ACCESS_KEY_ID)
AWS_SECRET_ACCESS_KEY=$(heroku config:get AWS_SECRET_ACCESS_KEY)
AWS_REGION=$(heroku config:get AWS_REGION)
S3_BUCKET_NAME=$(heroku config:get S3_BUCKET_NAME)

# Get the queryset for MissionArea
#missions=$(heroku run python -c "from home.models import MissionArea; missions = MissionArea.objects.all()")

# replacing S3_BUCKET_NAME, and ensuring arts-humanities is named correctly in DEV
if [ ENV_NAME == "dev" ]; then
    echo "Updating S3 object URLs for dev environment"
    python manage.py shell <<EOF
from home.models import MissionArea
missions = MissionArea.objects.all()
for mission in missions:
  url = mission.mission_image_url
  current = url[8:14]
  updated_url = url[0:17] + url[27:]
  updated_url = updated_url.replace(current, S3_BUCKET_NAME)
  updated_url = updated_url.replace("venus-blk", "arts-humanities-culture-venus-blk")
  mission.mission_image_url = updated_url
  mission.save()
EOF

# replacing S3_BUCKET_NAME, and ensuring arts-humanities is named correctly in CAT
if [ ENV_NAME == "cat" ]; then
    echo "Updating S3 object URLs for cat environment"
    python manage.py shell <<EOF
from home.models import MissionArea
missions = MissionArea.objects.all()
for mission in missions:
  url = mission.mission_image_url
  current = url[8:14]
  updated_url = url[0:17] + url[27:]
  updated_url = updated_url.replace(current, S3_BUCKET_NAME)
  updated_url = updated_url.replace("venus-blk", "arts-humanities-culture-venus-blk")
  mission.mission_image_url = updated_url
  mission.save()
EOF

# replacing S3_BUCKET_NAME, and ensuring arts-humanities is named correctly in PROD
if [ ENV_NAME == "prod" ]; then
    echo "Updating S3 object URLs for prod environment"
    python manage.py shell <<EOF
from home.models import MissionArea
missions = MissionArea.objects.all()
for mission in missions:
  url = mission.mission_image_url
  current = url[8:14]
  updated_url = url[0:17] + url[27:]
  updated_url = updated_url.replace(current, S3_BUCKET_NAME)
  updated_url = updated_url.replace("venus-blk", "arts-humanities-culture-venus-blk")
  mission.mission_image_url = updated_url
  mission.save()
EOF
