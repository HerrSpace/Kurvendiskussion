#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ✓

__author__  = "Patrick Meyer"
__email__   = "git@the-space.agency"

import collections

class Function(object):
	def __init__(self, faktoren):
		self.faktoren = faktoren #starts with x^0 x^1 .. x^n

	def __str__(self):
		vi = ""
		for idx, faktor in enumerate(self.faktoren):
			if idx == 0:
				vi = str(faktor)
			else:
				vi = "%s*x^%s + "%(faktor, idx) + vi

		return vi

	def Y(self, xVal):
		yVal = 0
		for idx, faktor in enumerate(self.faktoren):
			yVal += faktor * pow(xVal, idx)

		return yVal

	def integrieren(self): 
		fneu = []

		# This ignores the unknown part of the Integral
		fneu.append(0)

		for idx, faktor in enumerate(self.faktoren):
			fneu.append(faktor/(idx+1))

		return Function(fneu)
			
	def ableiten(self):
		fneu = []
		for idx, faktor in enumerate(self.faktoren):
			if idx == 0:
				continue
			fneu.append(idx * faktor)

		return Function(fneu)

	def nullstellen(self):
		idns = []

		f = self
		while f._newton() != None:
			idns.append(f._newton())
			f = f._horner()

		return idns

	def extrema(self):
		extrema = {
			"Hochpunkte": [],
			"Tiefpunkte": []
		}

		fa  = self.ableiten()
		faa = fa.ableiten()
		for ex in fa.nullstellen():
			if faa.Y(ex) != 0:
				if faa.Y(ex) > 0:
					extrema["Tiefpunkte"].append(ex)
				elif faa.Y(ex) < 0:
					extrema["Hochpunkte"].append(ex)
				else:
					pass # meh 

		return extrema

	def wendepunkte(self):
		wendepunkte = []
		faa = self.ableiten().ableiten()
		faaa = faa.ableiten()

		for ex in faa.nullstellen():
			if faaa.Y(ex) != 0:
				wendepunkte.append(ex)

		return wendepunkte

	def _newton(self):
		started = self.Y(-100) > 0
		idn = None

		for idxY in range(-100,100, 1):
			if (self.Y(idxY) > 0) != started:
				idn = idxY
				break

		if not idn:
			return idn

		idnOld = 9000
		while abs(idn - idnOld) > 0.000001:
			idnOld = idn

			zaehler = self.Y(idn)
			nenner = self.ableiten().Y(idn)

			if nenner == 0:
				return idn
			else:
				idn = idn - ( zaehler / nenner )

		return idn

	def _horner(self):
		idn = self._newton()
		nfaktoren = []

		for idx, faktor in enumerate(reversed(self.faktoren)):
			if idx == 0: # first
				nfaktoren.append(faktor)
			else:
				offset = nfaktoren[-1] * idn
				nfaktoren.append(faktor + offset)

		assert(nfaktoren[-1] < 0.001)
		nfaktoren = nfaktoren[:-1]

		return Function(list(reversed(nfaktoren)))


if __name__ == '__main__':
	fn = Function([0,8,-6,1])
#	fn = Function([2,0,1])
	print(fn)
	print(fn.integrieren())
	print(fn.extrema())
	print(fn.wendepunkte())
