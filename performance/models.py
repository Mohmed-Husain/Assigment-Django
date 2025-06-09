from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from employees.models import Employee

class Performance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performances')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review_date = models.DateField()
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['employee', 'review_date']
        
    def __str__(self):
        return f"{self.employee.name} - {self.review_date} - Rating: {self.rating}"

# Create your models here.
