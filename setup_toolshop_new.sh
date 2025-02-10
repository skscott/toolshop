#!/bin/bash

# Set project name
PROJECT_NAME="ToolShop"
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Do not run this script as root! Exiting."
    exit 1
fi

DJANGO_PROJECT="config"

# Define apps with their models
APPS=("users" "customers" "jobs" "invoices" "inventory" "settings")

# Detect OS and install necessary dependencies
echo "Detecting operating system..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux. Checking package manager..."
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y python3-dev default-libmysqlclient-dev build-essential pkg-config libpq-dev
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3-devel mysql-devel gcc pkg-config postgresql-devel
    elif command -v pacman &> /dev/null; then
        sudo pacman -S python python-pip mariadb-libs base-devel pkg-config
    else
        echo "Unsupported Linux distribution. Install dependencies manually."
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install mysql pkg-config postgresql
else
    echo "Unsupported OS. Please install dependencies manually."
    exit 1
fi

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install django djangorestframework django-environ django-cors-headers mysqlclient psycopg2

# Ask which database to use
echo "Choose your database:"
echo "1) MariaDB"
echo "2) PostgreSQL"
read -p "Enter choice (1 or 2): " DB_CHOICE

if [ "$DB_CHOICE" == "1" ]; then
    DB_ENGINE="django.db.backends.mysql"
    DB_PORT="3306"
    echo "Please create the database and user manually before proceeding:"
    echo "1. Log in to MySQL as root:"
    echo "   mysql -u root -p"
    echo "2. Run the following SQL commands:"
    echo "   DROP DATABASE IF EXISTS toolshop;"
    echo "   CREATE DATABASE toolshop;"
    
    echo "   CREATE USER IF NOT EXISTS 'toolshop_user'@'localhost' IDENTIFIED BY '7xGenaaid!';"
    echo "   GRANT ALL PRIVILEGES ON toolshop.* TO 'toolshop_user'@'localhost';"
    echo "   CREATE USER 'toolshop_user'@localhost IDENTIFIED BY '7xGenaaid!';" 
    echo "   GRANT ALL PRIVILEGES ON *.* TO 'toolshop_user'@localhost IDENTIFIED BY '7xGenaaid!';"
    echo "   GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY '7xGenaaid!' WITH GRANT OPTION;"
    
    echo "   FLUSH PRIVILEGES;"
    read -p "Press ENTER when you have completed these steps."
elif [ "$DB_CHOICE" == "2" ]; then
    DB_ENGINE="django.db.backends.postgresql"
    DB_PORT="5432"
    echo "Please create the database and user manually before proceeding:"
    echo "1. Log in to PostgreSQL as postgres:"
    echo "   sudo -u postgres psql"
    echo "2. Run the following SQL commands:"
    echo "   DROP DATABASE IF EXISTS toolshop;"
    echo "   DROP USER IF EXISTS toolshop_user;"
    echo "   CREATE DATABASE toolshop;"
    echo "   CREATE USER toolshop_user WITH PASSWORD '7xGenaaid!';"
    echo "   GRANT ALL PRIVILEGES ON DATABASE toolshop TO toolshop_user;"
    read -p "Press ENTER when you have completed these steps."
else
    echo "Invalid choice. Exiting."
    exit 1
fi

# Set DB credentials
DB_NAME="toolshop"
DB_USER="toolshop_user"
DB_PASSWORD="7xGenaaid!"  # Change before running

# Create Django project
django-admin startproject $DJANGO_PROJECT .

# Update settings.py to use .env file
# Ensure django-environ and os are imported at the top of settings.py
sed -i "1s/^/import environ\nimport os\n/" config/settings.py

# Replace existing DATABASES config in settings.py
sed -i '/^DATABASES =/,/^}/d' config/settings.py

# Insert new DATABASES config
cat <<EOL >> config/settings.py

# Load environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DATABASES = {
    'default': {
        'ENGINE': env("DB_ENGINE", default="django.db.backends.mysql"),
        'NAME': env("DB_NAME", default="toolshop"),
        'USER': env("DB_USER", default="toolshop_user"),
        'PASSWORD': env("DB_PASSWORD", default="7xGenaaid!"),
        'HOST': env("DB_HOST", default="localhost"),
        'PORT': env("DB_PORT", default="3306")
    }
}
EOL

# Create .env file
cat <<EOL > .env
DEBUG=True
SECRET_KEY=$(openssl rand -base64 32)
ALLOWED_HOSTS=localhost,127.0.0.1
DB_ENGINE=$DB_ENGINE
DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=$DB_PORT
EOL

# Create Django apps
for app in "${APPS[@]}"; do
    django-admin startapp $app
    mkdir -p $app/migrations
    touch $app/models.py $app/serializers.py $app/views.py $app/urls.py
    
    # Generate models.py
    echo "from django.db import models

class ${app^}(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
" > $app/models.py

    # Generate serializers.py
    echo "from rest_framework import serializers
from .models import ${app^}

class ${app^}Serializer(serializers.ModelSerializer):
    class Meta:
        model = ${app^}
        fields = '__all__'
" > $app/serializers.py

    # Generate views.py
    echo "from rest_framework import viewsets
from .models import ${app^}
from .serializers import ${app^}Serializer

class ${app^}ViewSet(viewsets.ModelViewSet):
    queryset = ${app^}.objects.all()
    serializer_class = ${app^}Serializer
" > $app/views.py

    # Generate urls.py
    echo "from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ${app^}ViewSet

router = DefaultRouter()
router.register(r'${app}', ${app^}ViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
" > $app/urls.py

done

# Add to settings.py
cat <<EOL >> config/settings.py
INSTALLED_APPS += [
    'rest_framework',
    'corsheaders',
    'users',
    'customers',
    'jobs',
    'invoices',
    'inventory',
    'settings',
]
EOL

echo "Adding DRF settings to settings.py..."

cat <<EOL >> toolshop/settings.py

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
}

# Authentication settings
LOGIN_URL = '/api-auth/login/'
LOGIN_REDIRECT_URL = "/api/"
EOL

echo "DRF settings added successfully!"

# Update config/urls.py
echo "from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
" > config/urls.py

for app in "${APPS[@]}"; do
    echo "    path('api/$app/', include('$app.urls'))," >> config/urls.py
done

echo "]" >> config/urls.py

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser prompt
read -p "Do you want to create a superuser now? (y/n): " CREATE_SUPERUSER
if [ "$CREATE_SUPERUSER" == "y" ]; then
    python manage.py createsuperuser
fi

# Create API Test Script
cat <<EOL > test_api.sh
#!/bin/bash
echo "Testing API endpoints..."
curl -X GET http://127.0.0.1:8000/api/users/ -H "Content-Type: application/json"
curl -X GET http://127.0.0.1:8000/api/jobs/ -H "Content-Type: application/json"
curl -X GET http://127.0.0.1:8000/api/invoices/ -H "Content-Type: application/json"
curl -X GET http://127.0.0.1:8000/api/inventory/ -H "Content-Type: application/json"
curl -X GET http://127.0.0.1:8000/api/settings/ -H "Content-Type: application/json"
curl -X GET http://127.0.0.1:8000/api/synclogs/ -H "Content-Type: application/json"
echo "API test complete."
EOL

chmod +x test_api.sh

echo "Setup complete! Run 'python manage.py runserver' to start the application."
