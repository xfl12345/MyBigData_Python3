import json
import os
import jschon

root_path = os.path.abspath(os.path.dirname(__file__)).split("mybigdata")[0]
print(root_path)
print(os.getcwd())

# with open(root_path + "mybigdata/src/test/test.json", "r", encoding="utf-8") as f:
#     testJsonInDict = json.loads(f.read())
# print(testJsonInDict)
#
# with open(root_path + "mybigdata/src/main/resources/json/schema/base_request_object.json", "r", encoding="utf-8") as f:
#     jsonSchemaInDict = json.loads(f.read())
# print(jsonSchemaInDict)
#
# catalogue = jschon.Catalogue.create_default_catalogue("2020-12")
# apiJsonSchema = jschon.JSONSchema(jsonSchemaInDict)
# jsonObject = jschon.JSON(testJsonInDict)
#
# print( jsonObject )
# print("**********************")
# print( apiJsonSchema.validate() )
# print(apiJsonSchema.evaluate( jsonObject ).valid)

with open(root_path + "mybigdata/src/main/resources/json/conf/mybigdata_configuration.json", "r", encoding="utf-8") as f:
    testJsonInDict = json.loads(f.read())
print(testJsonInDict)

with open(root_path + "mybigdata/src/main/resources/json/schema/mybigdata_configuration.json", "r", encoding="utf-8") as f:
    jsonSchemaInDict = json.loads(f.read())
print(jsonSchemaInDict)

print("**********************")
catalogue = jschon.Catalogue.create_default_catalogue("2020-12")
jsonSchema = jschon.JSONSchema(jsonSchemaInDict)
jsonObject = jschon.JSON(testJsonInDict)

ssss = json.dumps(testJsonInDict)
print(ssss)
print(jschon.JSON.loads(ssss))

print("**********************")
print( jsonObject )
print(jsonSchema.validate())
print(jsonSchema.evaluate(jsonObject).valid)

print("**********************")
json_schema_name = str(jsonSchema.get("title"))
print(json_schema_name)