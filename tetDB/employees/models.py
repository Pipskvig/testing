from django.db import models

# Create your models here.

class Employee(models.Model):
	name = models.CharField(max_length=200)
	company_name = models.CharField(max_length=100)
	position_name = models.CharField(max_length=100)
	hire_date = models.DateField()
	fire_date = models.DateField(blank=True, null=True)
	salary = models.IntegerField()
	fraction = models.IntegerField()
	base = models.IntegerField()
	advance = models.IntegerField()
	by_hours = models.BooleanField()
	
	def __str__(self):
		return self.name
