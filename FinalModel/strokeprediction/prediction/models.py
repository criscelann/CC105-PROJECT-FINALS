from django.db import models

class PredictionResult(models.Model):
    gender = models.CharField(max_length=10)  # 'Male' or 'Female'
    age = models.IntegerField()
    hypertension = models.BooleanField()
    heart_disease = models.BooleanField()
    ever_married = models.BooleanField()
    work_type = models.CharField(max_length=50)  # 'Private', 'Self-employed', 'Govt_job', 'Children', 'Never_worked'
    residence_type = models.CharField(max_length=50)  # 'Urban' or 'Rural'
    avg_glucose_level = models.FloatField()
    bmi = models.FloatField()
    smoking_status = models.CharField(max_length=50)  # 'never smoked', 'formerly smoked', 'smokes'
    prediction = models.CharField(max_length=50)  # "At risk" or "Not at risk"
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Prediction on {self.created_at}"