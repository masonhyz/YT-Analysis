from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import xgboost as xgb
from sklearn.model_selection import train_test_split
from wrangling import videos
import pandas as pd


# Example DataFrame columns
columns = ['categoryName', 'publishDay', 'publishHour', 'durationSeconds', 'caption', 'definition', 'dimension',
            'tags', 'favorites', 'comments', 'dislikes', 'likes', 'loggedViews']

videos_ml = videos.drop(columns=videos.columns.difference(columns), axis=1)  # Assuming 'views' is the target
videos_ml = pd.get_dummies(videos_ml, columns=['categoryName', 'caption', 'definition', 'dimension', 'tags',
                                               'publishDay'])

# Drop rows with missing target values
videos_ml = videos_ml.dropna(subset=['loggedViews'])
print(videos_ml.info())

# # Optionally, fill missing feature values
# videos[features] = videos[features].fillna(videos[features].mean())

features = videos_ml.columns.difference(['loggedViews'])

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(videos_ml[features], videos_ml['loggedViews'], test_size=0.2,
                                                    random_state=42)

# Random Forest model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)

# Evaluate the model
rf_mse = mean_squared_error(y_test, rf_predictions)
print(f"Random Forest MSE: {rf_mse}")


# XGBoost model
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100, learning_rate=0.1, random_state=42)
xgb_model.fit(X_train, y_train)
xgb_predictions = xgb_model.predict(X_test)

# Evaluate the model
xgb_mse = mean_squared_error(y_test, xgb_predictions)
print(f"XGBoost MSE: {xgb_mse}")


X_train_clean, X_test_clean = X_train.dropna(), X_test.dropna()
# GLM model (using Linear Regression as an example of GLM)
glm_model = LinearRegression()
glm_model.fit(X_train, y_train)
glm_predictions = glm_model.predict(X_test)

# Evaluate the model
glm_mse = mean_squared_error(y_test, glm_predictions)
print(f"GLM MSE: {glm_mse}")


