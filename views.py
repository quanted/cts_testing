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
import logging
# from cts_app.cts_api import cts_rest
from django.http import StreamingHttpResponse
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.conf import settings
# from ..cts_calcs.calculator import Calculator
from ..cts_calcs.calculator_test import TestWSCalc


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

	html += render_to_string('cts_export.html', {}, request=request)  # carries csrf token

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
				header = list(row_obj.keys())[0]  # list() addition for py3 fix
				if not header in headers:
					headers.append(header)
				header_index = headers.index(header)
				csv_data_row.insert(header_index, row_obj[header])
			csv_rows.append(csv_data_row)

		csv_rows.insert(0, headers)
		response = StreamingHttpResponse((writer.writerow(row) for row in csv_rows),
			content_type="text/csv")

		jid = TestWSCalc().gen_jid()  # create timestamp
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
	<div id="export_menu">
	  <ul>
		<li id="csvTESTWSExport"><a href="#" id="fadeExport_csv"></a><span></span></li>
	  </ul>
	</div> <!-- End "export_menu" div -->
	"""

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

	html += """
	<br><br>
	<h3>Response:</h3>
	<textarea id="testws-response" cols=60 rows=20></textarea>
	<br><br>
	"""

	html += render_to_string('cts_downloads.html', {'run_data': 'null'})

	html += '<link rel="stylesheet" href="//code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css">'  # need this for progress bar to show?
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

	html = html + render_to_string('cts_export.html', {}, request=request)

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


def create_testws_csv(request):
	"""
	CSV creation for TESTWS /testing/testws page
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

		testws_data = json.loads(request.POST['csv_data'])  # each row from rows is list of header:val objects
		pseudo_buffer = Echo()
		writer = csv.writer(pseudo_buffer)

		# build headers list for ordering values:
		accepted_cheminfo_keys = ['smiles', 'formula', 'iupac', 'mass', 'exactMass']  # chem info keys
		accepted_testws_keys = ['expVal', 'expValMass', 'predVal', 'predValMass']  # testws response keys
		
		_methods_map = {
			'Hierarchical clustering': 'hc',
			'FDA': 'fda',
			'Group contribution': 'gc',
			'Nearest neighbor': 'nn'
			# sm - single mode returning error still
		}

		_headers = []
		_batch_chems = []

		for _bc in testws_data['batch_chems']:
			_bc = _bc.replace('\r', '')
			_batch_chems.append(_bc)

		csv_rows = []
		_smiles_list = []

		for chem_name in _batch_chems:

			csv_data_row = []

			for chem_obj in testws_data['batch_data']:

				_smiles = chem_obj['node']['smiles']  # CTS-filtered SMILES

				# logging.warning("data iupac: {}".format(chem_obj['iupac']))

				if _smiles == chem_name:

					if not _smiles in csv_data_row:
						# looping chem info for single chemical object:
						for chem_info_key in accepted_cheminfo_keys:
							# want them ordered like accepted keys list..
							for key, val in chem_obj['node'].items():

								if key == chem_info_key:

									if not key in _headers:
										_headers.append(key)

									csv_data_row.append(val)

					# header ex: melting_point (testws, hc) predVal
					for testws_key in accepted_testws_keys:

						_method_header = _methods_map.get(chem_obj['data']['method'])
						_testws_datum = chem_obj['data']['predictions'][0][testws_key]

						header = "{} ({}, {}) {}".format(chem_obj['prop'], chem_obj['calc'], _method_header, testws_key)

						if not header in _headers:
							_headers.append(header)

						csv_data_row.append(_testws_datum)  # for now, all data as json in one column

			csv_rows.append(csv_data_row)

		csv_rows.insert(0, _headers)

		response = StreamingHttpResponse((writer.writerow(row) for row in csv_rows),
			content_type="text/csv")

		jid = TestWSCalc().gen_jid()  # create timestamp
		time_str = datetime.datetime.strptime(jid, '%Y%m%d%H%M%S%f').strftime('%A, %Y-%B-%d %H:%M:%S')

		response['Content-Disposition'] = 'attachment;filename=' + "cts_pchem_unittest" + '_' + jid + '.csv'
		return response

	return some_streaming_csv_view(request)