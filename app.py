# 1. import 
from flask import Flask, jsonify, request
from network_functions import setupUndirHeroGraph, getSankeyResult

app = Flask(__name__)

# initialize the undirected hero graph
undir_hero_graph = setupUndirHeroGraph()


"""
Enable CORS. Disable it if you don't need CORS
https://parzibyte.me/blog

Note: May need more expansive & fine-grained control over endpoints in the future!
"""
# @app.after_request
# def after_request(response):
#     response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
#     # response.headers["Access-Control-Allow-Credentials"] = "true"
#     response.headers["Access-Control-Allow-Methods"] = "GET"#"POST, GET, OPTIONS, PUT, DELETE"
#     response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
#     return response


@app.route("/api/sankey", methods=['GET'])
def get_sankey_data():
    try:
        args = request.args
        print(args)
        hero1 = request.args.get("hero1")
        hero2 = request.args.get("hero2")

        output_json = getSankeyResult(hero1, hero2, undir_hero_graph)

        response = jsonify(output_json)

        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        
    except:
        response = None

    return response
    


if __name__ == "__main__":
    app.run(debug=False)


