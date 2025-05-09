from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.timezone import now
import pickle
import os
from .models import PredictionResult


def load_model():
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'stroke_model.pkl')
        print(f"Looking for model file at: {model_path}")
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        return model_data['model']
    except FileNotFoundError:
        raise FileNotFoundError(f"Model file not found at: {model_path}")


def prediction_view(request):
    model = load_model()
    prediction = None

    if request.method == 'POST':
        try:
            # Extract form data
            age = int(request.POST.get('age'))
            gender = request.POST.get('gender', 'Male')  # Only Male or Female allowed
            hypertension = bool(int(request.POST.get('hypertension', 0)))
            heart_disease = bool(int(request.POST.get('heart_disease', 0)))
            ever_married = bool(int(request.POST.get('ever_married', 0)))
            work_type = request.POST.get('work_type', 'Private')
            residence_type = request.POST.get('residence_type', 'Urban')
            avg_glucose_level = float(request.POST.get('avg_glucose_level'))
            bmi = float(request.POST.get('bmi'))
            smoking_status = request.POST.get('smoking_status', 'never smoked')

            # Match the trained model's feature order
            input_features = [
                age,
                int(hypertension),
                int(heart_disease),
                avg_glucose_level,
                bmi
            ]

            # Predict stroke
            prediction = model.predict([input_features])[0]
            prediction_result = "At risk of stroke" if prediction == 1 else "Not at risk"

            # Save to database
            PredictionResult.objects.create(
                age=age,
                gender=gender,
                hypertension=hypertension,
                heart_disease=heart_disease,
                ever_married=ever_married,
                work_type=work_type,
                residence_type=residence_type,
                avg_glucose_level=avg_glucose_level,
                bmi=bmi,
                smoking_status=smoking_status,
                prediction=prediction_result,
                created_at=now()
            )

            # Redirect to result page
            return redirect(
                reverse('prediction_result') + f'?{urlencode({"prediction_result": prediction_result})}'
            )

        except ValueError as e:
            return render(request, 'prediction_form.html', {
                'error': f'Invalid input: {str(e)}. Please check your data.'
            })
        except Exception as e:
            return render(request, 'prediction_form.html', {
                'error': f'An error occurred: {str(e)}'
            })

    return render(request, 'prediction_form.html')


def prediction_result_view(request):
    prediction_result = request.GET.get('prediction_result', 'No result')
    return render(request, 'prediction_result.html', {'prediction': prediction_result})


# def admin_dashboard(request):
#     results = PredictionResult.objects.all().order_by('-created_at')
#     return render(request, 'admin_dashboard.html', {'results': results})

# def dashboard(request):
#     # Logic for your dashboard view
#     return render(request, 'dashboard.html')

from django.db.models import Count, Q
from .models import PredictionResult

def dashboard(request):
    results = PredictionResult.objects.all().order_by('-created_at')
    total_patients = results.count()
    strokes = results.filter(prediction="At risk of stroke").count()

    return render(request, 'dashboard.html', {
        'predictionresult': results,
        'total_patients': total_patients,
        'strokes': strokes
    })
