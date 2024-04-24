from tree import JavaASTGenerator
from ExtractValues import ExtractValues
from Summarize import Summarizer
from Catagorize import Labeler
from Similarity import Similarity
from dotenv import load_dotenv
from populateDB import PopulateDB
import os

load_dotenv()
api_key = os.getenv('OPENAI_KEY')

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
    summarizer = Summarizer(api_key)
    classSummary = summarizer.summarizeClass(OUTPUT_DIR+'/Documentation.json', outputPath=OUTPUT_DIR+'/ClassSummary.json')
    print(classSummary)
    functionSummary = summarizer.summarizeFunctions(OUTPUT_DIR+'/Functions.json', outputPath=OUTPUT_DIR+'/FunctionSummary.json')
    print(functionSummary)
    labeler = Labeler(api_key)
    classDomains = labeler.getClassDomain(OUTPUT_DIR+'/Documentation.json', outputPath=OUTPUT_DIR+'/ClassDomains.json')
    print(classDomains)
    functionDomains = labeler.getFunctionDomain(OUTPUT_DIR+'/Functions.json', outputPath=OUTPUT_DIR+'/FunctionDomains.json')
    print(functionDomains)
    similarity = Similarity()
    similarities = similarity.getSimilarities(OUTPUT_DIR+'/Documentation.json', outputPath=OUTPUT_DIR+'/Similarities.json')
    print(similarities)
    return OUTPUT_DIR

# loop through java file and generate report for each file
# for file in os.listdir('java'):
#     if file.endswith('.java'):
#         outputfile = GenerateReport('java/'+file)
#         PopulateDB(outputfile).populate()



outputfile = GenerateReport('java/Sample.java')
PopulateDB(outputfile).populate()
PopulateDB('Sample_outputs').populate()