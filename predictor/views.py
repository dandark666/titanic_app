from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import joblib
import pandas as pd

# ================================
# Cargar modelo previamente entrenado
# ================================
model = joblib.load("titanic_model.pkl")

# Precisión conocida (puedes guardarla cuando entrenas el modelo)
accuracy = 79.5  # ejemplo, cambia según tu entrenamiento

# ================================
# Vistas Django
# ================================
def index(request):
    return render(request, "index.html", {"accuracy": accuracy})

@csrf_exempt
def predict(request):
    if request.method == "POST":
        try:
            # Mapear datos del formulario
            data = {
                'Pclass': int(request.POST['Pclass']),
                'Sex': 1 if request.POST['Sex']=='male' else 0,
                'Age': float(request.POST['Age']),
                'SibSp': int(request.POST['SibSp']),
                'Parch': int(request.POST['Parch']),
                'Fare': float(request.POST['Fare']),
                'Embarked': {'C':0,'Q':1,'S':2}[request.POST['Embarked']]
            }

            df_input = pd.DataFrame([data])

            # Predicción
            pred = model.predict(df_input)[0]

            # Resultado para template
            resultado = "Sobrevivirá ✅" if pred==1 else "No sobrevivirá ❌"

            return render(request, "index.html", {"prediction": resultado, "accuracy": accuracy, "pred": pred})

        except Exception as e:
            return render(request, "index.html", {"prediction": f"Error: {str(e)}", "accuracy": accuracy})
    
    return render(request, "index.html", {"accuracy": accuracy})