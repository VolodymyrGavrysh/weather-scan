from django.test import TestCase
import inspect
from apps.ml.registry import MLRegistry
from apps.ml.income_classifier.random_forest import RandomForestClassifier
# from apps.ml.income_classifier.extra_tree import ExtraTreesClassifier
# from apps.ml.income_classifier.cat_boost import CatBoostClassifier

from django.test import TestCase
from rest_framework.test import APIClient


class MLTests(TestCase):

    ## TEST ONE

    def test_rf_algorithm(self):

        input_data = {"Location_ID": 1,
                     "Cloud9am": 0.0,
                     "Cloud3pm": 3.0,
                     "Humidity9am": 17.0,
                     "Humidity3pm": 16.0,
                     "Pressure9am": 1010.5,
                     "Pressure3pm": 1005.8,
                     "MinTemp": 19.6,
                     "MaxTemp": 37.6,
                     "Temp9am": 30.4,
                     "Temp3pm": 37.2,
                     "Rainfall": 0.0,
                     "Evaporation": 11.2,
                     "Sunshine": 9.8,
                     "WindGustDir": 13,
                     "WindGustSpeed": 87.0,
                     "WindDir9am": 1,
                     "WindDir3pm": 2,
                     "WindSpeed9am": 20.0,
                     "WindSpeed3pm": 11.0,
                     "year": 2008,
                     "month": 12,
                     "season": 1}

        my_alg = RandomForestClassifier()
        response = my_alg.compute_prediction(input_data)
        print('-----------')
        print(response)
        print(f'classiyer is working and prediction is {response}')
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual('No Rain', response['label'])

#     ## TEST TWO

    # def test_registry(self):
    #     registry = MLRegistry()
    #     self.assertEqual(len(registry.endpoints), 0)
    #     endpoint_name = "income_classifier"
    #     algorithm_object = RandomForestClassifier()
    #     algorithm_name = "random forest"
    #     algorithm_status = "production"
    #     algorithm_version = "0.0.1"
    #     algorithm_owner = "Vlad"
    #     algorithm_description = "Random Forest with simple pre- and post-processing"
    #     algorithm_code = inspect.getsource(RandomForestClassifier)
    #     # add to registry
    #     registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name,
    #                 algorithm_status, algorithm_version, algorithm_owner,
    #                 algorithm_description, algorithm_code)
    #     # there should be one endpoint available
    #     self.assertEqual(len(registry.endpoints), 1)

    #     print(f'algoritm endpoints {registry.endpoints}')

#     ## TEST THREE

#     def test_et_algorithm(self):

#         input_data = {"MaxTemp": 34.3, "Location_ID": 11}

#         my_extra_tree = ExtraTreesClassifier()
#         response = my_extra_tree.compute_prediction(input_data)
#         print('-----------')
#         print(f' ExtraTreesClassifier classiyer is working and prediction is {response}')
#         # self.assertEqual('OK', response['status'])
#         self.assertTrue('label' in response)
#         self.assertEqual('No Rain', response['label'])


#     def test_et_algorithm(self):

#         input_data = {"MaxTemp": 34.3, "Location_ID": 11}

#         my_extra_tree = CatBoostClassifier()
#         response = my_extra_tree.compute_prediction(input_data)
#         print('-----------')
#         print(f' CatBoostClassifier classiyer is working and prediction is {response}')
#         # self.assertEqual('OK', response['status'])
#         self.assertTrue('label' in response)
#         self.assertEqual('No Rain', response['label'])



# class EndpointTests(TestCase):

#     def test_predict_view(self):
#         client = APIClient()

#         input_data = {
#             "MaxTemp": 13.8,
#             "Location_ID": 33}

#         classifier_url = "/api/v1/income_classifier/predict"
#         response = client.post(classifier_url, input_data, format='json')
#         self.assertEqual(response.status_code, 200)
#         print(response)
#         # self.assertEqual(response.data["label"], "Rain")
#         self.assertTrue("request_id" in response.data)
#         self.assertTrue("status" in response.data)

