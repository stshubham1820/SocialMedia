from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,mobile,password=None,**extra_fields):
        if not mobile :
            raise ValueError("Mobile No is Required")
        user = self.model(mobile=mobile,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,mobile,password=None,**extra_fields) :
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Super User Must have is_staff True")
        return self.create_user(mobile,password,**extra_fields)