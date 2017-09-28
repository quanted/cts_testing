from django.conf.urls import url
# from django.contrib import admin
# admin.autodiscover()
from ..cts_testing import views


urlpatterns = [
	# (r'^/?$', 'views.getCTSEndpoints'),

	url(r'^$', views.validationTestPage),
	# url(r'^$', views.validationTestPage),
	url(r'^csv/?$', views.createCSV),
	url(r'^testws/?$', views.test_ws_page),
	# url(r'^output/?$', views.unitTestsOutputPage)
	# url(r'^swag/?$', views.getSwaggerJsonContent),
	# url(r'^docs/?$', cts_rest.showSwaggerPage),

	# url(r'^molecule/?$', cts_rest.getChemicalEditorData),
	# url(r'^speciation/?$', cts_rest.getChemicalEditorData),

	# url(r'^(?P<calc>.*?)/inputs/?$', views.getCalcInputs),
	# url(r'^(?P<calc>.*?)/run/?$', views.runCalc),
	# url(r'^(?P<endpoint>.*?)/?$', views.getCalcEndpoints),
]