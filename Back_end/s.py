from decouple import config
print(config("DATABASE_USER"))  # Should print 'postgres'
