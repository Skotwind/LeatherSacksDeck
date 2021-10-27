from django.db import models

GENDER = [
    ('male', 'male'),
    ('female', 'female'),
    ('h', 'helicopter'),
]

POSITION = [
    ('m', 'manager'),
    ('w', 'worker'),
]


class Skill(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.title}"


class HardSkill(Skill):
    value = models.FloatField(editable=False, default=1)

    def __str__(self):
        return f"{self.title}"


class SoftSkill(Skill):
    def __str__(self):
        return f"{self.title}"


class UserInfo(models.Model):
    name = models.CharField(max_length=20)
    sur_name = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER)
    experience = models.FloatField(null=True, blank=True)
    birthplace = models.TextField(max_length=200, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    height = models.FloatField(max_length=220, null=True, blank=True)
    weight = models.FloatField(max_length=220, null=True, blank=True)
    hard_skills = models.ManyToManyField(HardSkill, null=True)
    soft_skills = models.ManyToManyField(SoftSkill, null=True)

    class Meta:
        unique_together = ('name', 'sur_name')

    def __str__(self):
        return f"{self.name} {self.sur_name}"


class Manager(models.Model):
    title = models.CharField(max_length=30)
    info = models.OneToOneField(UserInfo, on_delete=models.CASCADE, primary_key=True, unique=True)

    def __str__(self):
        return f"{self.info.name} {self.info.sur_name}"


class Worker(models.Model):
    title = models.CharField(max_length=30)
    info = models.OneToOneField(UserInfo, on_delete=models.CASCADE, primary_key=True, unique=True)
    warden = models.ForeignKey(Manager, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return f"{self.info.name} {self.info.sur_name}"
