import json
import os
import jschon

print(os.getcwd())

with open("src/test/test.json", "r", encoding="utf-8") as f:
    testJsonStr = json.loads(f.read())
print(testJsonStr)


with open("src/main/resources/json/schema/base_request_object.json", "r", encoding="utf-8") as f:
    jsonSchemaStr = json.loads(f.read())
print(jsonSchemaStr)

catalogue = jschon.Catalogue.create_default_catalogue("2020-12")
apiJsonSchema = jschon.JSONSchema(jsonSchemaStr)
jsonObject = jschon.JSON(testJsonStr)

print( jsonObject )
print(apiJsonSchema.evaluate( jsonObject ).valid)



