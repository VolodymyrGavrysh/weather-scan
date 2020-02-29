import joblib
import pandas as pd


class RandomForestClassifier:
    def __init__(self):
        path_to_artifacts = "apps/ml/income_classifier/"
        # self.values_fill_missing =  joblib.load(path_to_artifacts + "train_mode.joblib")
        # self.encoders = joblib.load(path_to_artifacts + "encoders.joblib")
        self.model = joblib.load(path_to_artifacts + "xgb-tunning_model.pkl")

    def preprocessing(self, input_data):
        # JSON to pandas DataFrame
        input_data = pd.DataFrame(input_data, index=[0])

        return input_data

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def postprocessing(self, input_data):
        label = "No Rain"
        if input_data[1] > 0.4:
            label = "Rain"
        return {"probability": input_data[1], "label": label, "status": "OK"}

    def compute_prediction(self, input_data):

        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0] # only one sample
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction


# from sklearn.base import BaseEstimator, TransformerMixin

# # Vitaly
# class PredictProbaToTransform(BaseEstimator, TransformerMixin):
#     """
#     Give all X and classifier on input
#     output - predict_proba by classifier (only binary classifier)
#     This class needs to compare outputs from classifiers in FeatureUnion model
#     """
#     def init(self, clf):
#         self.clf = clf

#     def fit(self, X, y=None):
#         return self

#     def transform(self, X):
#         output = self.clf.predict_proba(X)[:, 1]
#         output = np.reshape(output, (-1,1))

#         return output
