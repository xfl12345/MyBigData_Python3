import json
import os
import jschon

root_path = os.path.abspath(os.path.dirname(__file__)).split("mybigdata")[0]
print(root_path)
print(os.getcwd())

with open(root_path + "mybigdata/src/test/test.json", "r", encoding="utf-8") as f:
    testJsonStr = json.loads(f.read())
print(testJsonStr)

with open(root_path + "mybigdata/src/main/resources/json/schema/base_request_object.json", "r", encoding="utf-8") as f:
    jsonSchemaStr = json.loads(f.read())
print(jsonSchemaStr)

catalogue = jschon.Catalogue.create_default_catalogue("2020-12")
apiJsonSchema = jschon.JSONSchema(jsonSchemaStr)
jsonObject = jschon.JSON(testJsonStr)

print( jsonObject )
print(apiJsonSchema.evaluate( jsonObject ).valid)
