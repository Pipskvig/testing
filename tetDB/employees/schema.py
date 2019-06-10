import graphene

from graphene_django.types import DjangoObjectType
from tetDB.employees.models import Employee
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql_relay import from_global_id
from graphene import InputObjectType
from datetime import date, datetime

class EmployeeType(DjangoObjectType):
	class Meta:
		model = Employee

class EmployeeMutation(graphene.Mutation):
	class Arguments:
		name = graphene.String()
		company_name = graphene.String()
		position_name = graphene.String()
		hire_date = graphene.String()
		fire_date = graphene.String(required=False)
		salary = graphene.Int()
		fraction = graphene.Int()
		base = graphene.Int()
		advance = graphene.Int()
		by_hours = graphene.Boolean()

	employee = graphene.Field(EmployeeType)
	
	def mutate(self, info, **kwargs):
		try:
			employee = Employee.objects.get(name=kwargs['name'])
			employee.company_name = kwargs['company_name']
			employee.position_name = kwargs['position_name']
			employee.hire_date = datetime.strptime(kwargs['hire_date'], "%Y-%M-%d").date()
			#employee.fire_date = datetime.strptime(kwargs['fire_date'], "%Y-%M-%d").date()
			employee.salary = kwargs['salary']
			employee.fraction = kwargs['fraction']
			employee.base = kwargs['base']
			employee.advance = kwargs['advance']
			employee.by_hours = kwargs['by_hours']
			employee.save()
		except Employee.DoesNotExist:
			employee = Employee.objects.create(name=kwargs['name'],
			company_name=kwargs['company_name'],
			position_name=kwargs['position_name'],
			hire_date=datetime.strptime(kwargs['hire_date'], "%Y-%M-%d").date(),
			#fire_date=datetime.strptime(kwargs['fire_date'], "%Y-%M-%d").date(),
			salary=kwargs['salary'],
			fraction=kwargs['fraction'],
			base = kwargs['base'],
			advance=kwargs['advance'],
			by_hours = kwargs['by_hours'])
		
		return EmployeeMutation(employee=employee)
		
class SalaryMutation(graphene.Mutation):
	class Arguments:
		id = graphene.ID()
		salary = graphene.Int()
		fraction = graphene.Int()

	employee = graphene.Field(EmployeeType)
	
	def mutate(self, info, **kwargs):
		employee = Employee.objects.get(id=kwargs['id'])
		employee.salary = kwargs['salary']
		employee.fraction = kwargs['fraction']
		employee.save()
		
		return SalaryMutation(employee=employee)

class BaseMutation(graphene.Mutation):
	class Arguments:
		id = graphene.ID()
		base = graphene.Int()

	employee = graphene.Field(EmployeeType)
	
	def mutate(self, info, **kwargs):
		employee = Employee.objects.get(id=kwargs['id'])
		employee.base = kwargs['base']
		employee.save()
		
		return BaseMutation(employee=employee)

class AdvanceMutation(graphene.Mutation):
	class Arguments:
		id = graphene.ID()
		advance = graphene.Int()

	employee = graphene.Field(EmployeeType)
	
	def mutate(self, info, **kwargs):
		employee = Employee.objects.get(id=kwargs['id'])
		employee.advance = kwargs['advance']
		employee.save()
		
		
		return AdvanceMutation(employee=employee)

class ByHoursSwitchMutation(graphene.Mutation):
	class Arguments:
		id = graphene.ID()
		by_hours = graphene.Boolean()
	
	employee = graphene.Field(EmployeeType)
	
	def mutate(self, info, **kwargs):
		employee = Employee.objects.get(id=kwargs['id'])
		employee.by_hours = kwargs['by_hours']
		employee.save()
		
		return ByHoursSwitchMutation(employee=employee)

class FireMenMutation(graphene.Mutation):
	class Arguments:
		id = graphene.ID()
	
	employee = graphene.Field(EmployeeType)
	
	def mutate(self, info, **kwargs):
		employee = Employee.objects.get(id=kwargs['id'])
		employee.fire_date = date.today()
		employee.save()
		
		return FireMenMutation(employee=employee)

class Mutation:
	employee_mutation = EmployeeMutation.Field()
	salary_mutation = SalaryMutation.Field()
	base_mutation = BaseMutation.Field()
	advance_mutation = AdvanceMutation.Field()
	by_hours_switch_mutation = ByHoursSwitchMutation.Field()
	fire_men_mutation = FireMenMutation.Field()

class Query(graphene.ObjectType):
	all_employees = graphene.List(EmployeeType)
	get_employee = graphene.Field(EmployeeType, name=graphene.String())
	get_not_fired_employees = graphene.List(EmployeeType)
	
	def resolve_all_employees(self, info):
		return Employee.objects.all()
	
	def resolve_get_employee(self, info, **kwargs):
		name = kwargs.get('name')
		
		if name is not None:
			return Employee.objects.get(name=name)
		
		return None

	def resolve_get_not_fired_employees(self, info):
		return Employee.objects.filter(fire_date=None)
