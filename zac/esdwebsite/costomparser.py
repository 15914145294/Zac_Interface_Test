# encoding:utf-8

from esdwebsite.access import AccessApply
from configs.ad09config import ESD_PRODUCTS
from html.parser import HTMLParser


class CustomParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self._events = dict()
		self._flag = None
		self._product = []

	def handle_starttag(self, tag, attrs):
		try:
			if tag == "input" and attrs.__contains__(('class', "btn btn-primary btn-xl")):
				product = self._attr(attrs, "onclick")
				self._product.append(product)
		except:
			raise AttributeError("The tag not contain onclick event")

	# def handle_data(self, data):
	# 	if self._flag == 'input':
	# 		# self._events[self._count][self._flag] = data
	# 	# if self._flag == 'time':
	# 	# 	self._events[self._count][self._flag] = data
	# 	# if self._flag == 'event-location':
	# 	# 	self._events[self._count][self._flag] = data
	# 	# self._flag = None
	# 		print(data)

	def _attr(self, attr_list, attr_name):
		for attr in attr_list:
			if attr_name == attr[0]:
				return attr[1]
			else:
				continue

	def products(self):
		for x in ESD_PRODUCTS:
			for j in self._product:
				if x.__str__().lower() in j:
					index = self._product.index(j)
					self._product[index] = x
				else:
					continue
		return self._product

# s = AccessApply().obj[1]
# html = AccessApply().SelectProduct()[1]


def get_products(html):
	parser = CustomParser()
	parser.feed(html)
	# print (parser.products())
	parser.close()
	return parser.products()


# MATCHED_PRODUCTS = get_products(html)
# if __name__ == '__main__':
# 	pass
