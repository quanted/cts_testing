"""
Testing views - p-chem unit tests, and
eventually more!
Dec. 2016
"""
__author__='np'

from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string


def unitTestsInputPage(request, model='none', header='CTS'):
	"""
	Shows p-chem table (html, css, js)
	"""
	html = render_to_string('01cts_uberheader.html', {'title': header+' Unit Tests'})
	html = html + render_to_string('04uberbatchinput.html', {
	            'model': model,
	            'model_attributes': header+' Unit Tests'})
	html += render_to_string('04uberinput_jquery.html', { 'model': model}) # loads scripts_pchemprop.js
	html = html + render_to_string('04uberbatchinput_jquery.html', {'model':model, 'header':header})
	html = html + render_to_string('06cts_uberfooter.html', {'links': ''})
	
	response = HttpResponse()
	response.write(html)
	return response