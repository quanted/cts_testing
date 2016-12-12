"""
Testing views - p-chem unit tests, and
eventually more!
Dec. 2016
"""
__author__='np'

from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.conf import settings


def unitTestsPage(request, model='pchemprop', header='CTS'):
	"""
	Shows p-chem table (html, css, js)
	"""
	html = render_to_string('cts_testing/01cts_uberheader.html', {'title': header+' Unit Tests'})
	html += render_to_string('cts_testing/04uberbatchinput.html', {
				'model': model,
				'model_attributes': header+' Unit Tests'})
	html += render_to_string('cts_testing/04uberinput_jquery.html', { 'model': model}) # loads scripts_pchemprop.js

	html += render_to_string('cts_testing/cts_pchem.html')

	# html += '<br><br><button type="button" id="submit" hidden style="float:right;padding:4px;"> Run unit test </button><br>'
	html += """
		<div class="input_nav">
			<div class="input_right">
				<input type="button" value="Clear" id="clearbutton" class="input_button">
				<input class="submit input_button" type="button" value="Submit">
			</div>
		</div>
	</div>
	"""

	html += render_to_string('cts_downloads.html', {'run_data': 'null'})

	html += '<link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">'
	# for pchemprop batch, use p-chem for selecting inputs for batch data:
	html +=  render_to_string('cts_pchemprop_requests.html', 
		{
			'checkedCalcsAndProps': {},
			'kow_ph': 7.4,
			'speciation_inputs': 'null',
			'nodes': 'null',
			'nodejs_host': settings.NODEJS_HOST,
			'nodejs_port': settings.NODEJS_PORT
		}
	)
	html += render_to_string('cts_gentrans_tree.html', {'gen_max': 0})

	html += render_to_string('cts_testing/cts_pchem_tests.html', {'model':model, 'header':header})

	html += render_to_string('cts_testing/06cts_uberfooter.html', {'links': ''})
	
	response = HttpResponse()
	response.write(html)
	return response