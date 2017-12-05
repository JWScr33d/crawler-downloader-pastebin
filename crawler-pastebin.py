#!/usr/bin/env python
# -*- coding: utf-8 -*-

#AUTHOR: JORGE CORONADO aka @JorgeWebsec
#License: GNU
#WEB: blog.quantika14.com
#Description: fork Pyctionary(https://github.com/sylm87/pyctionary) to download all pastebin

import urllib2, re, mechanize, cookielib, time, os, requests, base64
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient(connect=False)
db = client.Dante


long_max = 8    # 12 caracteres de longitud máxima de claves de diccionario (por defecto)
long_min = 8     # 4 caracteres de longitud minima por defecto

char_null = ['']
chars_min = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
chars_may = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
chars_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
chars_spe = ['.', '-', '_', '/', '@']

# añadimos los caracteres que permitimos para generar el diccionario
permitidos = []
permitidos += char_null
permitidos += chars_min
#permitidos += chars_may
permitidos += chars_num
#print permitidos

total_chars = len(permitidos)
char_n_max = total_chars - 1
print total_chars

cadena = []

for chars in range(0, long_max):
	cadena += [0]
 
#print cadena

for i in range (1, long_min+1):
	cadena[-(i)] = 1

cadena_max = []
for chars in range(0, long_max):
	cadena_max += [ total_chars -1 ]


#********************FUNCIONES*********************
def toClave(cadena1):
 	password = ""
 	for indice in cadena1:
  		password += permitidos[indice]
 	return password
 

def isMax(cadena1):
	if toClave(cadena1) != toClave(cadena_max):
  		return False

	return True
 
 
def aumentarCadena(cadena1):
	unidad = 1
	acarreo = 0
	for digito in range(1,long_max +1):
  #time.sleep( 0.1 ) # para debug
  		if cadena[-(digito)] < char_n_max:
   			if unidad == 1:
   				cadena[-(digito)] += 1
   				unidad = 0
    			return cadena1
   			elif acarreo == 1:
    			cadena[-(digito)] += 1
    			acarreo = 0
    			return cadena1
  		else: 
   			cadena[-(digito)] = 1
   			acarreo = 1
 			return cadena1

def insert_mongodb(dict_paste):
	db.Pastebin.update({"url":dict_paste["url"], "data":dict_paste["data"]},dict_paste,True)
	return True
def main():
	print "WELCOME TO DOWNLOAD PASTEBIN"
	print "			by @JorgeWebsec"
	
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
	return TAG_RE.sub('', text)
	
if __name__ == '__main__':
	main()
	bucle = True
	while bucle:
		url_base = "https://pastebin.com/"
		password = toClave(cadena)
		url = url_base + password
		print url
		try:
			response = requests.get(url)
		except:
			print "[ERROR] connection reset by peer..."
		html = response.text
		soup = BeautifulSoup(html, "html.parser")
		
		data = soup.find("div",{"id":"selectable"})
		if data:
			data = str(remove_tags(data))
			info_user = soup.find("div", {"class":"paste_box_line2"}).text.split("\n")
			dict_paste={"url":url,"user":info_user[1].strip(), "date":info_user[2].strip(), "data":data}
			insert_mongodb(dict_paste)
			print "[URL][>] " + url + " DOWNLOAD..."
		else:
			print "[URL][>] " + url + "[INFO] No existe la url o ha sido eliminado..."
		if isMax(cadena):
		 	bucle = False
		cadena = aumentarCadena(cadena)
