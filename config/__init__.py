import os
# If using PyMySQL as a drop-in replacement for MySQLdb, install it here.
try:
	import pymysql
	pymysql.install_as_MySQLdb()
except Exception:
	# Don't fail import if PyMySQL isn't installed; settings will control DB backend.
	pass

