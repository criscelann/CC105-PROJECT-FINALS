import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.inspection import permutation_importance
import pandas as pd

# Load the real stroke dataset
def load_stroke_data():
    df = pd.read_csv('cleaned_stroke_data.csv')
    return df

# Load dataset
stroke_df = load_stroke_data()

# Define your feature columns based on your actual dataset
feature_columns = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi']
X = stroke_df[feature_columns].values
y = stroke_df['stroke'].values

# 1. Check for class imbalance
print("Class distribution:")
print(stroke_df['stroke'].value_counts(normalize=True))

# 2. Train-test split with stratification
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 3. Initialize the RandomForest model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=7,
    min_samples_leaf=10,
    class_weight='balanced',
    random_state=42
)

# 4. Train the model
model.fit(X_train, y_train)

# 5. Evaluate performance
print("\nModel evaluation:")
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred, target_names=['No Stroke', 'Stroke']))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print(f"\nROC AUC Score: {roc_auc_score(y_test, y_proba):.3f}")

# 6. Feature importance using permutation
print("\nFeature importances:")
result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)
for i in result.importances_mean.argsort()[::-1]:
    print(f"{feature_columns[i]:<20}: {result.importances_mean[i]:.3f}")

# 7. Save model with metadata
model_info = {
    'model': model,
    'feature_columns': feature_columns,
    'training_data_stats': {
        'class_distribution': dict(stroke_df['stroke'].value_counts()),
        'feature_means': dict(stroke_df[feature_columns].mean()),
        'feature_stds': dict(stroke_df[feature_columns].std())
    },
    'evaluation_metrics': {
        'classification_report': classification_report(y_test, y_pred, output_dict=True),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
        'roc_auc': roc_auc_score(y_test, y_proba)
    }
}

with open('stroke_model.pkl', 'wb') as f:
    pickle.dump(model_info, f)

print("\nStroke prediction model saved successfully with metadata!")
