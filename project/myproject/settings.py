import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myApp',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'myApp/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
       

 },
    },
]

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
DEBUG = True


# PostgreSQL veritabanı ayarları
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',  # Veritabanı adınızı buraya girin
        'USER': 'postgres',  # Veritabanı kullanıcı adınızı buraya girin
        'PASSWORD': '123456',  # Veritabanı şifrenizi buraya girin
        'HOST': 'localhost',  # Veritabanı host adresi (genellikle localhost)
        'PORT': '5432',  # PostgreSQL varsayılan portu
    }
}