#!/bin/bash
# -- encoding:utf-8 --
import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time,types,copy
from datetime import datetime

from aiohttp import web

listA = [1,[2],3,4,5]
'''
	print(list)
'''
def log(func):
	def wrapper(*args,**kw):
		print("excute %s:" % func.__name__)
		return func(*args,**kw)
	return wrapper

@log
def now():
	print("2016-12-09")

now()
print("函数：")
print(type(now)==types.FunctionType)
print("lambda:")
print(type(lambda x:x)==types.LambdaType)


def shallow_copy(str1):
	return copy.copy(str1)

def test_copy():
	print("浅拷贝前：{}".format(listA))
	listB = shallow_copy(listA)
	print("浅拷贝后：{}".format(listB))
	listA.append(3)
	listA[1].append(9)
	print(listA)
	print(listB)
	
test_copy()




def index(request):
	return web.Response(body=b'<h1>Hello World!Awesome.</h1>',content_type='text/html', charset='UTF-8')

@asyncio.coroutine
def init(loop):
	app = web.Application(loop=loop)
	app.router.add_route('GET', '/', index)
	srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
	logging.info('server started at http://127.0.0.1:9000...')
	return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

@asyncio.coroutine
def create_pool(loop, **kw):
	logging.info('create database connection pool...')
	global __pool
	__pool = yield from aiomysql.create_pool(
		host=kw.get('host', 'localhost'),
		port=kw.get('port', 3306),
		user=kw['root'],
		password=kw['root'],
		db=kw['python'],
		charset=kw.get('charset', 'utf8'),
		autocommit=kw.get('autocommit', True),
		maxsize=kw.get('maxsize', 10),
		minsize=kw.get('minsize', 1),
		loop=loop
	)