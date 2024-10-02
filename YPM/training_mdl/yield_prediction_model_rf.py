import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load the dataset
data = pd.read_csv('yield_df.csv')

# Select features and target variable
X = data[['Area', 'Item', 'average_rain_fall_mm_per_year', 'avg_temp', 'pesticides_tonnes']]
y = data['hg/ha_yield']

# Define the preprocessing for the categorical features
categorical_features = ['Area', 'Item']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Define the preprocessing for the numerical features
numerical_features = ['average_rain_fall_mm_per_year', 'avg_temp', 'pesticides_tonnes']
numerical_transformer = StandardScaler()

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features),
        ('num', numerical_transformer, numerical_features)
    ])

# Define the RandomForestRegressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Create a pipeline that first preprocesses the data and then fits the RandomForestRegressor model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', model)
])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the pipeline
pipeline.fit(X_train, y_train)

# Save the entire pipeline
joblib.dump(pipeline, 'models/randomforest_pipeline.pkl')

# Evaluate the model
y_pred = pipeline.predict(X_test)
print(f"Mean Squared Error: {mean_squared_error(y_test, y_pred)}")
print(f"R-squared Score: {r2_score(y_test, y_pred)}")

print("Model training complete. Model saved.")
