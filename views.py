"""
Testing views - p-chem validation tests, and
eventually more!
Dec. 2016
"""
__author__='np'
import csv
import json
import datetime
import os
# from cts_app.cts_api import cts_rest
from django.http import StreamingHttpResponse
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.conf import settings
from ..cts_calcs.calculator import Calculator


def validationTestPage(request, model='pchemprop', header='CTS'):
	"""
	Shows p-chem table (html, css, js)
	"""
	html = render_to_string('cts_testing/01cts_uberheader.html', {'title': header+' Unit Tests'})
	html += render_to_string('cts_testing/04uberbatchinput.html', {
				'model': model,
				'model_attributes': '{} {} Validation Tests'.format(header, model)})
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
			'kow_ph': 7.0,
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


def createCSV(request):
	"""
	Creates CSV for p-chem unit test data,
	with input csv data, cts web service data,
	and percent difference.
	"""

	class Echo(object):
		"""
		An object that implements just the write method of the file-like
		interface.
		"""
		def write(self, value):
			"""Write the value by returning it, instead of storing in a buffer"""
			return value

	def some_streaming_csv_view(request):
		"""A view that streams a large CSV file"""
		# Generate a sequence of rows. The range is based on the max num of
		# rows that can be handled by a single sheet in most spreadsheet apps.
		# rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))

		rows = json.loads(request.POST['csv_data'])  # each row from rows is list of header:val objects
		pseudo_buffer = Echo()
		writer = csv.writer(pseudo_buffer)

		# build headers list for ordering values:
		headers = []
		# for row_obj in rows[0]:
		# 	headers.append(row_obj.keys()[0])

		csv_rows = []
		for row in rows:
			csv_data_row = []
			# row is list of header:val for that chemical
			for row_obj in row:
				header = row_obj.keys()[0]
				if not header in headers:
					headers.append(header)
				header_index = headers.index(header)
				csv_data_row.insert(header_index, row_obj[header])
			csv_rows.append(csv_data_row)

		csv_rows.insert(0, headers)
		response = StreamingHttpResponse((writer.writerow(row) for row in csv_rows),
			content_type="text/csv")

		jid = Calculator().gen_jid()  # create timestamp
		time_str = datetime.datetime.strptime(jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')

		response['Content-Disposition'] = 'attachment;filename=' + "cts_pchem_unittest" + '_' + jid + '.csv'
		return response

	return some_streaming_csv_view(request)


def test_ws_page(request):
	"""
	TEST WS testing page at /cts/rest/testws
	"""

	#drupal template for header with bluestripe
	#html = render_to_string('01epa_drupal_header.html', {})
	html = render_to_string('01epa_drupal_header.html', {
		'SITE_SKIN': os.environ['SITE_SKIN'],
		'title': "CTS"
	})

	html += render_to_string('02epa_drupal_header_bluestripe_onesidebar.html', {})
	html += render_to_string('03epa_drupal_section_title_cts.html', {})

	html += render_to_string('06cts_ubertext_start_index_drupal.html', {
		# 'TITLE': 'Calculate Chemical Speciation',
		# 'TEXT_PARAGRAPH': xx
	})

	# inputPageFunc = getattr(inputmodule, model+'InputPage')  # function name = 'model'InputPage  (e.g. 'sipInputPage')
	# html += inputPageFunc(request, model, header)
	html += render_to_string('04cts_uberbatchinput.html', {
			'model': 'TESTWS',
			'model_attributes': 'TEST WS Batch Run'}, request=request)
	html += render_to_string('04cts_uberbatchinput_jquery.html', {'model':'TESTWS', 'header': ""})

	html += render_to_string('04cts_uberinput_jquery.html', { 'model': "pchemprop"}) # loads scripts_pchemprop.js

	# html += render_to_string('cts_testing/cts_pchem_testws.html')
	# html += render_to_string('cts_testws_page.html', {})
	html += """
	<div id="pchem_batch_wrap" hidden>
		<h3>Select p-chem properties for batch chemicals</h3>
	"""

	html += render_to_string('cts_testing/cts_pchem_testws.html', {})

	html += """
		<div class="input_nav">
			<div class="input_right">
				<input type="button" value="Clear" id="clearbutton" class="input_button">
				<input class="testws-submit input_button" type="submit" value="Submit">
			</div>
		</div>
	</div>
	"""

	html += render_to_string('07ubertext_end_drupal.html', {})
	# html += ordered_list(model='cts/' + model, page='input')

	#scripts and footer
	html += render_to_string('09epa_drupal_ubertool_css.html', {})
	html += render_to_string('09epa_drupal_cts_css.html')

	# sending request to template with scripts_jchem added (will this work if template imports js and isn't in template itself?)
	html += render_to_string('09epa_drupal_cts_scripts.html', request=request)
	html += render_to_string('10epa_drupal_footer.html', {})
  
	response = HttpResponse()
	response.write(html)
	return response