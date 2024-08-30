from django.db import models


class XX(models.Model):
    title = models.CharField(verbose_name="Title", max_length=32)
    image = models.FileField(verbose_name="Avatar", upload_to="avatar/")


class Admin(models.Model):
    """ Administrator """
    username = models.CharField(verbose_name="Username", max_length=32)
    password = models.CharField(verbose_name="Password", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """ Department Table """
    title = models.CharField(verbose_name='Title', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ Employee Table """
    name = models.CharField(verbose_name="Name", max_length=16)
    password = models.CharField(verbose_name="Password", max_length=64)
    age = models.IntegerField(verbose_name="Age")
    account = models.DecimalField(verbose_name="Account Balance", max_digits=10, decimal_places=2, default=0)
    # create_time = models.DateTimeField(verbose_name="Entry Time")
    create_time = models.DateField(verbose_name="Entry Time")

    # No Constraint
    # depart_id = models.BigIntegerField(verbose_name="Department ID")
    # 1. With Constraint
    #   - to: Reference to the table
    #   - to_field: Reference to the column in the table
    # 2. Django Automatic
    #   - depart is written
    #   - Generates data column depart_id
    # 3. When Department Table is Deleted
    # ### 3.1 Cascade Delete
    depart = models.ForeignKey(verbose_name="Department", to="Department", to_field="id", on_delete=models.CASCADE)
    # ### 3.2 Set Null
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # Constraints in Django
    gender_choices = (
        (1, "Male"),
        (2, "Female"),
    )
    gender = models.SmallIntegerField(verbose_name="Gender", choices=gender_choices)


class PrettyNum(models.Model):
    """ Pretty Number Table """
    mobile = models.CharField(verbose_name="Mobile Number", max_length=11)
    # To allow null values, use null=True, blank=True
    price = models.IntegerField(verbose_name="Price", default=0)

    level_choices = (
        (1, "Level 1"),
        (2, "Level 2"),
        (3, "Level 3"),
        (4, "Level 4"),
    )
    level = models.SmallIntegerField(verbose_name="Level", choices=level_choices, default=1)

    status_choices = (
        (1, "Occupied"),
        (2, "Unused")
    )
    status = models.SmallIntegerField(verbose_name="Status", choices=status_choices, default=2)


class Task(models.Model):
    """ Task """
    level_choices = (
        (1, "Urgent"),
        (2, "Important"),
        (3, "Temporary"),
    )
    level = models.SmallIntegerField(verbose_name="Level", choices=level_choices, default=1)
    title = models.CharField(verbose_name="Title", max_length=64)
    detail = models.TextField(verbose_name="Details")

    # user_id
    user = models.ForeignKey(verbose_name="Person in Charge", to="Admin", on_delete=models.CASCADE)


class Order(models.Model):
    """ Order """
    oid = models.CharField(verbose_name="Order Number", max_length=64)
    title = models.CharField(verbose_name="Title", max_length=32)
    price = models.IntegerField(verbose_name="Price")

    status_choices = (
        (1, "Pending Payment"),
        (2, "Paid"),
    )
    status = models.SmallIntegerField(verbose_name="Status", choices=status_choices, default=1)
    # admin_id
    admin = models.ForeignKey(verbose_name="Administrator", to="Admin", on_delete=models.CASCADE)


class Boss(models.Model):
    """ Boss """
    name = models.CharField(verbose_name="Name", max_length=32)
    age = models.IntegerField(verbose_name="Age")
    img = models.CharField(verbose_name="Avatar", max_length=128)


class City(models.Model):
    """ City """
    name = models.CharField(verbose_name="Name", max_length=32)
    count = models.IntegerField(verbose_name="Population")

    # Essentially, it's a CharField in the database, automatically saving the data.
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')

