import os
import re

from django.template.loader import get_template
from django.template import Context, TemplateSyntaxError

from django.test import TestCase
from django.test.utils import override_settings

from fest.template import JSError


FEST_ROOT = os.path.join(os.path.dirname(__file__), 'static/fest')

class FestTestCase(TestCase):
	def setUp(self):
		pass

	def test_doctype(self):
		"""doctype"""
		tmpl = 'doctype.xml'
		ctxt = {}
		html = '<!DOCTYPE html>'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_text(self):
		"""text"""
		tmpl = 'text.xml'
		ctxt = {}
		html = '  '
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_short_tag(self):
		"""short tag"""
		tmpl = 'shorttag.xml'
		ctxt = {}
		html = '<meta/>'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_comment(self):
		"""comment"""
		tmpl = 'comment.xml'
		ctxt = {}
		html = '<!--comment-->'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_value(self):
		"""value"""
		tmpl = 'value.xml'
		ctxt = {"value":"value"}
		html = 'value<script/>\\"|\\\''
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_if(self):
		"""if"""
		tmpl = 'if.xml'
		ctxt = {}
		html = 'truetrue&'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_choose(self):
		"""choose"""
		tmpl = 'choose.xml'
		ctxt = {}
		html = 'truechoose'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_for(self):
		"""for"""
		tmpl = 'for.xml'
		ctxt = {}
		html = 'foo=bar'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_foreach(self):
		"""foreach"""
		tmpl = 'foreach.xml'
		ctxt = {'items': [1, 2], 'subitems':[[1, 2], [1, 2]]}
		html = '120102111245'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_script(self):
		"""script"""
		tmpl = 'script.xml'
		ctxt = {}
		html = '"true""true"'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_insert(self):
		"""insert"""
		tmpl = 'insert.xml'
		ctxt = {}
		html = '<style>.foo{ont: 18px/18px "Helvetica Neue", Arial;}\n.bar{\\"\\"}</style>'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_use_strict(self):
		"""use strict"""
		tmpl = 'strict.xml'
		ctxt = {}
		with self.assertRaises(JSError) as error:
			res = get_template(tmpl).render(Context(ctxt))
		self.assertEqual(str(error.exception), 'g is not defined')

	def test_blocks(self):
		"""blocks"""
		tmpl = 'blocks.xml'
		ctxt = {}
		html = 'start|one|two2|three1|five|six|seven|eight|finish'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_params(self):
		"""params"""
		tmpl = 'params.xml'
		ctxt = {}
		html = 'Hello, John'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_include(self):
		"""include"""
		tmpl = 'include.xml'
		ctxt = {}
		with self.assertRaises(JSError) as error:
			res = get_template(tmpl).render(Context(ctxt))
		self.assertTrue(str(error.exception).startswith('error open file '))
		self.assertTrue(str(error.exception).endswith(' No such file or directory'))

	def test_cdata(self):
		"""CDATA"""
		tmpl = 'cdata.xml'
		ctxt = {}
		html = '<script><![CDATA[alert ("2" < 3);]]></script>'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_setparams(self):
		"""setparams"""
		tmpl = 'setparams.xml'
		ctxt = {}
		html = '|text1||text2||text3||text4|'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_attribute(self):
		"""attribute"""
		tmpl = 'attribute.xml'
		ctxt = {}
		html = '<input/><div>foobar</div><div class="foo bar"></div><div class="foo"></div><div when="true" otherwise="true"></div><div>foo</div>'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_first_attributes(self):
		"""first attributes"""
		tmpl = 'first_attributes.xml'
		ctxt = {}
		with self.assertRaises(Exception) as error:
			res = get_template(tmpl).render(Context(ctxt))
		self.assertTrue(str(error.exception).startswith('JSError:'))
		r = re.compile('^At line 5: fest:attributes must be the first child', re.M)
		self.assertTrue(r.search(str(error.exception)) is not None)

	def test_nested_attributes(self):
		"""nested attributes"""
		tmpl = 'nested_attributes.xml'
		ctxt = {}
		with self.assertRaises(Exception) as error:
			res = get_template(tmpl).render(Context(ctxt))
		self.assertTrue(str(error.exception).startswith('JSError:'))
		r = re.compile('^At line 5: fest:attributes cannot be nested', re.M)
		self.assertTrue(r.search(str(error.exception)) is not None)

	def test_document_write(self):
		"""document.write"""
		tmpl = 'document.xml'
		ctxt = {}
		html = 'foobarbar'
		self.assertEqual(get_template(tmpl).render(Context(ctxt)), html)

	def test_unclosed_template(self):
		"""unclosed template"""
		tmpl = 'template.xml'
		ctxt = {}
		with self.assertRaises(Exception) as error:
			res = get_template(tmpl).render(Context(ctxt))
		self.assertTrue(str(error.exception).startswith('JSError:'))
		r = re.compile('^At line 2: fest:template is not closed', re.M)
		self.assertTrue(r.search(str(error.exception)) is not None)


FestTestCase = override_settings(
	TEMPLATE_DEBUG=True,
	FEST_ROOT=FEST_ROOT,
	FEST_LIB_ROOT=os.path.join(FEST_ROOT, 'lib'),
	FEST_TEMPLATES_ROOT=os.path.join(FEST_ROOT, 'tests/templates'),
	TEMPLATE_DIRS=(os.path.join(FEST_ROOT, 'tests/templates'),)
)(FestTestCase)

