from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / 'data' / 'student_dropout_academic_success.csv'
MODEL_PATH = BASE_DIR / 'eduguard_model.pkl'

COLUMN_MAPPING = {
    'Marital status': 'marital_status',
    'Application mode': 'application_mode',
    'Application order': 'application_order',
    'Course': 'course',
    'Daytime/evening attendance	': 'daytime_attendance',
    'Previous qualification': 'previous_qualification',
    'Previous qualification (grade)': 'previous_qualification_grade',
    'Nacionality': 'nacionality',
    "Mother's qualification": 'mothers_qualification',
    "Father's qualification": 'fathers_qualification',
    "Mother's occupation": 'mothers_occupation',
    "Father's occupation": 'fathers_occupation',
    'Admission grade': 'admission_grade',
    'Displaced': 'displaced',
    'Educational special needs': 'educational_special_needs',
    'Debtor': 'debtor',
    'Tuition fees up to date': 'tuition_fees_up_to_date',
    'Gender': 'gender',
    'Scholarship holder': 'scholarship_holder',
    'Age at enrollment': 'age_at_enrollment',
    'International': 'international',
    'Curricular units 1st sem (credited)': 'cu1_credited',
    'Curricular units 1st sem (enrolled)': 'cu1_enrolled',
    'Curricular units 1st sem (evaluations)': 'cu1_evaluations',
    'Curricular units 1st sem (approved)': 'cu1_approved',
    'Curricular units 1st sem (grade)': 'cu1_grade',
    'Curricular units 1st sem (without evaluations)': 'cu1_without_evaluations',
    'Curricular units 2nd sem (credited)': 'cu2_credited',
    'Curricular units 2nd sem (enrolled)': 'cu2_enrolled',
    'Curricular units 2nd sem (evaluations)': 'cu2_evaluations',
    'Curricular units 2nd sem (approved)': 'cu2_approved',
    'Curricular units 2nd sem (grade)': 'cu2_grade',
    'Curricular units 2nd sem (without evaluations)': 'cu2_without_evaluations',
    'Unemployment rate': 'unemployment_rate',
    'Inflation rate': 'inflation_rate',
    'GDP': 'gdp',
}

FEATURE_ORDER = list(COLUMN_MAPPING.values())
TARGET_COLUMN = 'Target'
POSITIVE_CLASS = 'Dropout'


def load_dataset():
    df = pd.read_csv(DATA_PATH, sep=';')
    df = df.rename(columns=COLUMN_MAPPING)
    return df


def train_model():
    df = load_dataset()
    missing_columns = set(FEATURE_ORDER) - set(df.columns)
    if missing_columns:
        raise RuntimeError(f'Missing dataset columns: {sorted(missing_columns)}')

    X = df[FEATURE_ORDER].astype(float).fillna(0)
    y = (df[TARGET_COLUMN] == POSITIVE_CLASS).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = make_pipeline(
        StandardScaler(),
        GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=5,
            random_state=42,
        ),
    )
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    print('Training complete')
    print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
    print(f'ROC AUC: {roc_auc_score(y_test, y_proba):.4f}')
    print('Classification report:')
    print(classification_report(y_test, y_pred, target_names=['not_dropout', 'dropout']))

    joblib.dump(pipeline, MODEL_PATH)
    print(f'Model saved to {MODEL_PATH}')


if __name__ == '__main__':
    train_model()
