import unittest
import os.path
from mako.template import Template
from yacg.builder.jsonBuilder import getModelFromJson
from yacg.model.config import BlackWhiteListEntry, BlackWhiteListEntryTypeEnum
import yacg.generators.helper.generatorHelperFuncs as generatorHelper

import yacg.model.config as config


class TestOpenApi (unittest.TestCase):
    def testYacgModel(self):
        modelFile = 'resources/models/json/yacg_model_schema.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        modelTypes = getModelFromJson(model, [])
        templateFile = 'resources/templates/examples/openApiJson.mako'
        templateFileExists = os.path.isfile(templateFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameters = {}
        templateParameters['restTypes'] = 'ComplexType,Tag'
        template = Template(filename=templateFile)
        renderResult = template.render(modelTypes=modelTypes, templateParameters=templateParameters)
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/yacgModelOpenApi.json"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()

    def testKrakendTemplate(self):
        modelFile = 'tests/resources/models/json/examples/swagger_v2_example.json'
        modelFileExists = os.path.isfile(modelFile)
        self.assertTrue('model file exists: ' + modelFile, modelFileExists)
        model = config.Model()
        model.schema = modelFile
        ignorePathTypes = False
        modelTypes = getModelFromJson(model, [], ignorePathTypes)
        whiteList = []
        whiteListEntry = BlackWhiteListEntry()
        whiteListEntry.name = 'PathType'
        whiteListEntry.type = BlackWhiteListEntryTypeEnum.TYPETYPE
        whiteList.append(whiteListEntry)
        pathTypes = generatorHelper.trimModelTypes(modelTypes, (), whiteList)
        self.assertEqual(14, len(pathTypes))

        templateFile = 'resources/templates/examples/krakend.mako'
        templateFileExists = os.path.isfile(templateFile)
        self.assertTrue('template file exists: ' + templateFile, templateFileExists)
        templateParameters = {}
        template = Template(filename=templateFile)
        renderResult = template.render(modelTypes=modelTypes, templateParameters=templateParameters)
        self.assertIsNotNone(renderResult)

        testOutputFile = "tmp/krakend.json"
        f = open(testOutputFile, "w+")
        f.write(renderResult)
        f.close()
