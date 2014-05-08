DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'jacohen+dh',                      # Or path to database file if using sqlite3.
        'USER': 'jacohen',                      # Not used with sqlite3.
        'PASSWORD': 'lintax',                  # Not used with sqlite3.
        'HOST': 'sql.mit.edu',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
# Make this unique, and don't share it with anybody.
SECRET_KEY = '%rz*^s7r^&bsew,9w^cwzasdfqweasdffaasdf5!%i61gr659ov+vql1u9afcj$txy))sddmp'
# List of callables that know how to import templates from various sources.
