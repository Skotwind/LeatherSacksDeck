from django.db import models

GENDER = [
    ('m', 'male'),
    ('f', 'female'),
    ('h', 'helicopter'),
]

POSITION = [
    ('m', 'manager'),
    ('w', 'worker'),
]


class Skill(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=200)

    class Meta:
        abstract = True


class HardSkill(Skill):
    value = models.FloatField(editable=False, default=1)


class SoftSkill(Skill):
    pass


class Slave(models.Model):
    name = models.CharField(max_length=20)
    sur_name = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER)
    experience = models.FloatField(null=True, blank=True)
    birthplace = models.TextField(max_length=200, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    growth = models.FloatField(max_length=220, null=True, blank=True)
    weight = models.FloatField(max_length=220, null=True, blank=True)
    position = models.CharField(max_length=20, choices=POSITION)
    warden = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)
    hard_skills = models.ManyToManyField(HardSkill)
    soft_skills = models.ManyToManyField(SoftSkill)
