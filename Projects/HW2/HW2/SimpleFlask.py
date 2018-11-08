# Lahman.py

# Convert to/from web native JSON and Python/RDB types.
import json

# Include Flask packages
from flask import Flask
from flask import request
import copy

import SimpleBO

# The main program that executes. This call creates an instance of a
# class and the constructor starts the runtime.
app = Flask(__name__)

def parse_and_print_args():

    fields = None
    in_args = None
    if request.args is not None:
        in_args = dict(copy.copy(request.args))
        fields = copy.copy(in_args.get('fields', None))
        if fields:
            del(in_args['fields'])

        limit = copy.copy(in_args.get('limit', None))
        offset = copy.copy(in_args.get('offset', None))
        if limit:
            del in_args['limit']
            limit = limit[0]
        if offset:
            del in_args['offset']
            offset = offset[0]

    try:
        if request.data:
            body = json.loads(request.data)
        else:
            body = None
    except Exception as e:
        print("Got exception = ", e)
        body = None



    print("Request.args : ", json.dumps(in_args))
    print("in_args : ", in_args)
    print("fields : ", fields)
    print("body : ", body)
    print("limit : ", limit)
    print("offset : ", offset)
    return in_args, fields, body, limit, offset


@app.route('/api/<resource>', methods=['GET', 'POST'])
def get_resource(resource):


    in_args, fields, body, limit, offset = parse_and_print_args()
    if limit is None:
        limit = 10
    if offset is None:
        offset = 0

    if resource == "roster":
        if request.method == 'GET':
            result = SimpleBO.get_roster(in_args, limit, offset)
            result = [{'data':result}, {'links':paginate(request.url, limit, offset)}]
            print(result)
            


            if result:
                return json.dumps(result), 200, {'content-type':'application/json; charset: utf-8'}
            else:
                return "NOT FOUND", 404
        else:
            return "Method {} on resource {} not implemented!".format(request.method, resource), \
            501, {"content-type":"text/plain; charset: utf-8"}


    if request.method == 'GET':
        result = SimpleBO.find_by_template(resource, \
                                           in_args, fields)
        result = [{'data':result}, {'links':paginate(request.url, limit, offset)}]
        if result:
            result = [{'data':result}, {'links':paginate(request.url, limit, offset)}]
            return json.dumps(result), 200, \
               {"content-type": "application/json; charset: utf-8"}
        else:
            return "NOT FOUND", 404
    elif request.method == 'POST':
        result = SimpleBO.insert(resource, body)
        return json.dumps(result), 200, {"content-type": "application/json; charset: utf-8"}
    else:
        return "Method " + request.method + " on resource " + resource + \
               " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


@app.route('/api/<resource>/<primary_key>', methods=['GET', 'PUT', 'DELETE'])
def get_resource_by_primary_key(resource, primary_key):
    in_args, fields, body, limit, offset = parse_and_print_args()


    if request.method == "GET":
        result = SimpleBO.find_by_primary_key(resource, primary_key, fields)
        return json.dumps(result), 200, {"content-type":"application/json; charset: utf-8"}
    elif request.method == "PUT":
        result = SimpleBO.find_by_primary_key(resource, primary_key, fields)
        if result is not None:
            result = SimpleBO.delete(resource, primary_key)
            result = SimpleBO.insert_primary_key(resource, primary_key, body)
            result = SimpleBO.find_by_primary_key(resource, primary_key, fields)
            return json.dumps(result), 200, {"content-type":"application/json; charset: utf-8"}
        else:
            return "Error: record not found", 404
    elif request.method == "DELETE":
        try:
            result = SimpleBO.delete(resource, primary_key) 
            return json.dumps(result), 200, {"content-type":"application/json; charset: utf-8"}
        except:
            return "Error: record not found", 404
    else:
        return "Method " + request.method + " on resource " + resource + \
        " not implemented!", 501, {"content-type": "text/plain; charset: utf-8"}


@app.route('/api/<resource>/<primary_key>/<related_resource>', methods=['GET', 'POST'])
def get_related_resource(resource, primary_key, related_resource):
    in_args, fields, body, limit, offset = parse_and_print_args()

    if limit is None:
        limit = 10
    if offset is None:
        offset = 0

    if request.method == "GET":
        try:
            result = SimpleBO.find_related_resource(resource, primary_key, related_resource, in_args, fields)
        except:
            result = SimpleBO.find_related_resource2(resource, primary_key, related_resource, in_args, fields)
        if result:
            result = [{'data':result}, {'links':paginate(request.url, limit, offset)}]
            return json.dumps(result), 200, {"content-type":"application/json; charset: utf-8"}
        else:
            return "NOT FOUND", 404
    elif request.method == "POST":
        result = SimpleBO.insert_related_resource(resource, primary_key, related_resource, body, fields)
        return json.dumps(result), 200, {"content-type": "application/json; charset: utf-8"}
    else:
        return "Method {} on resource {} not implemented!".format(request.method, resource), \
        501, {"content-type":"text/plain; charset: utf-8"}


@app.route('/api/teammates/<playerid>', methods=['GET'])
def get_teammates(playerid):
    in_args, fields, body, limit, offset = parse_and_print_args()

    if request.method == 'GET':
        result = SimpleBO.get_teammates(playerid)
        if result:
            return json.dumps(result), 200, {'content-type':'application/json; charset: utf-8'}
        else:
            return "NOT FOUND", 404
    else:
        return "Method {} on resource {} not implemented!".format(request.method, resource), \
        501, {"content-type":"text/plain; charset: utf-8"}


@app.route('/api/people/<playerid>/career_stats', methods=['GET'])
def get_career_stats(playerid):
    in_args, fields, body, limit, offset = parse_and_print_args()

    if request.method == 'GET':
        result = SimpleBO.get_career_stats(playerid)
        print(result)
        if result:
            return json.dumps(result), 200, {'content-type':'application/json; charset: utf-8'}
        else:
            return "NOT FOUND", 404
    else:
        return "Method {} on resource {} not implemented!".format(request.method, resource), \
        501, {"content-type":"text/plain; charset: utf-8"}


def paginate(link, limit, offset):
    links, prev, nxt = [], {}, {}

    if int(offset) - int(limit) > 0:
        prev['prev'] = link.replace("&offset={}&limit={}".format(offset, limit), "&offset={}&limit={}".format(str(int(offset)-int(limit)), offset))
    else:
        prev['prev'] = "No link available"

    links.append(prev)

    nxtoff = int(offset) + int(limit)
    print("next", nxtoff)
    print(link)
    nxtlink = link.replace("&offset={}&limit={}".format(offset, limit), "&offset={}&limit={}".format(nxtoff, limit))

    nxt['next'] = nxtlink
    links.append(nxt)
    # if int(limit) + int(offset) <= total:
    #     links.append(nxt)
    # else:
    #     links.append({'next':"No link available"})

    return links





if __name__ == '__main__':
    app.run()

