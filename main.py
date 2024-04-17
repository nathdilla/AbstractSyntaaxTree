from tree import JavaASTGenerator
from ExtractValues import ExtractValues
from Summarize import Summarizer
from Catagorize import Labeler
from Similarity import Similarity
import os

API_KEY = 'sk-'

def GenerateReport(javaFile):
    filename = os.path.basename(javaFile).split('.')[0]
    OUTPUT_DIR = filename + '_outputs'
    # make output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    print("REPORT GENERATED IN: ", OUTPUT_DIR)
    
    ast_generator = JavaASTGenerator(javaFile)
    ast_generator.generate_ast_json(OUTPUT_DIR+'/AST.json')
    extract_values = ExtractValues(OUTPUT_DIR+'/AST.json')
    extract_values.extract(OUTPUT_DIR)
    summarizer = Summarizer(API_KEY)
    classSummary = summarizer.summarizeClass(OUTPUT_DIR+'/Documentation.json', outputPath=OUTPUT_DIR+'/ClassSummary.json')
    print(classSummary)
    functionSummary = summarizer.summarizeFunctions(OUTPUT_DIR+'/Functions.json', outputPath=OUTPUT_DIR+'/FunctionSummary.json')
    print(functionSummary)
    labeler = Labeler(API_KEY)
    classDomains = labeler.getClassDomain(OUTPUT_DIR+'/Documentation.json', outputPath=OUTPUT_DIR+'/ClassDomains.json')
    print(classDomains)
    functionDomains = labeler.getFunctionDomain(OUTPUT_DIR+'/Functions.json', outputPath=OUTPUT_DIR+'/FunctionDomains.json')
    print(functionDomains)
    similarity = Similarity()
    similarities = similarity.getSimilarities(OUTPUT_DIR+'/Documentation.json', outputPath=OUTPUT_DIR+'/Similarities.json')
    print(similarities)

GenerateReport('java/TaskManager.java')