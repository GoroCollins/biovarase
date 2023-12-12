from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Branch(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    description = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False, editable=False)
    created_by = models.ForeignKey(CustomUser, editable=False, null=False, on_delete=models.PROTECT, related_name='created_by', related_query_name='created_by')
    last_modified_at = models.DateTimeField(auto_now=True, editable=False, null=False)
    modified_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='modified_by', related_query_name='modified_by', null=False, editable=False)
    branch_manager = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=False)
    active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f'{self.description}'
class Section(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    description = models.CharField(max_length=100, null=False)
    branch = models.ForeignKey(Branch, null=False, on_delete=models.PROTECT, related_name='section', related_query_name='section')
    
    def __str__(self) -> str:
        return f'{self.description} lab'

class MeasuringMethod(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=100, null=False)
    active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f'{self.description}'

class Unit(models.Model):
    code = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=100, null=False)
    
    def __str__(self) -> str:
        return f'{self.description}'
class Equipment(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=100, null=False)
    location = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='location', related_query_name='location', null=False)
    section = models.ForeignKey(Section, on_delete=models.PROTECT, related_name='labsection', related_query_name='labsection', null=False)
    serial = models.CharField(max_length=100, null=False)
    in_use = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f'{self.description} at {self.location} for {self.section} section'
class Sample(models.Model):
    description = models.CharField(max_length=100, null=False)
    
    def __str__(self) -> str:
        return f'{self.description}'
class Analysis(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    description = models.CharField(max_length=200, null=False)
    section = models.ForeignKey(Section, related_name='analysis', related_query_name='analysis', on_delete=models.PROTECT, null=False)
    active = models.BooleanField(default=True)
    measuremethod = models.ForeignKey(MeasuringMethod, on_delete=models.PROTECT, related_name='method', related_query_name='method', null=False)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, related_name='equipment', related_query_name='equipment', null=False)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='analysis', related_query_name='analysis', null=False)
    sample = models.ForeignKey(Sample, on_delete=models.PROTECT, related_name='analysis', related_query_name='analysis', null=False)
    analytical_goals = ((0, 'CVw'), (1, 'CVb'), (2, 'Imp%'), (3, 'Bias%'), (4, 'TEa%'))
    analytical_goal = models.CharField(max_length=10, choices=analytical_goals, null=True)
    def __str__(self) -> str:
        return f'{self.description}'

class ControlLevel(models.Model):
    supplier = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=100, null=False)
    reference = models.CharField(max_length=100, null=False)
    active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f'{self.description} from {self.supplier} with reference {self.reference}'
    
class Batch(models.Model):
    control = models.ForeignKey(ControlLevel, on_delete=models.PROTECT, related_name='control', related_query_name='control', null=False)
    description = models.CharField(max_length=100, null=False)
    lot = models.CharField(max_length=100, null=False)
    expiration_date = models.DateField(null=False)
    target = models.CharField(max_length=50, null=False)
    lower = models.IntegerField(default=0)
    upper = models.IntegerField(default=0)
    standard_deviation = models.IntegerField(default=0)
    expired = models.BooleanField(default=False)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, related_name='batch', related_query_name='batch')
    active = models.BooleanField(default=True)
    def __str__(self) -> str:
        return f'Batch {self.description} for control {self.control} for lot {self.lot} with target {self.target} and expiry {self.expiration_date}'

class Result(models.Model):
    analysis = models.ForeignKey(Analysis, on_delete=models.PROTECT, related_name='analysis', related_query_name='analysis', null=False)
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT, related_name='equipment', related_query_name='equipment', null=False)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, related_name='batch', related_query_name='batch', null=False)
    value = models.IntegerField(default=0, null=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='created_by', related_query_name='related_by')
    modified_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='modifier', related_query_name='modifier', null=False)
    last_modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'Result for {self.analysis} for batch {self.batch} done on {self.equipment} equipment'

class Note(models.Model):
    action = models.CharField(max_length=3)
    description = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='created_by', related_query_name='created_by', null=False)
    
    def __str__(self) -> str:
        return f'{self.id}. {self.description}'

class Supplier(models.Model):
    pass
    
    
