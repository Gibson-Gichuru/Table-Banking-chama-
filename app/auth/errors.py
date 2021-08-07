
from flask import jsonify

def forbidden_errror(message):

	response = jsonify({"Error":"forbidden", "Message":message})
	response.status_code = 404

	return response


def unauthorised(message):

	response = jsonify({"Error":"unauthorised", "Message":"Not Authorised to view the requested resource"})

	response.status_code = 401

	return response