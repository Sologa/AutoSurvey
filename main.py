import os
import json
import argparse
from src.agents.outline_writer import outlineWriter
from src.agents.writer import subsectionWriter
from src.agents.judge import Judge
from src.database import database
from src.paper_provider import PaperProvider
from tqdm import tqdm
import time

def remove_descriptions(text):
    lines = text.split('\n')
    
    filtered_lines = [line for line in lines if not line.strip().startswith("Description")]
    
    result = '\n'.join(filtered_lines)
    
    return result

def write(topic, model, section_num, subsection_len, rag_num, refinement, paper_provider=None):
    outline, outline_wo_description = write_outline(topic, model, section_num, paper_provider=paper_provider)

    if refinement:
        raw_survey, raw_survey_with_references, raw_references, refined_survey, refined_survey_with_references, refined_references = write_subsection(topic, model, outline, subsection_len = subsection_len, rag_num = rag_num, paper_provider=paper_provider, refinement = True)
        return refined_survey_with_references
    else:
        raw_survey, raw_survey_with_references, raw_references = write_subsection(topic, model, outline, subsection_len = subsection_len, rag_num = rag_num, paper_provider=paper_provider, refinement = False)
        return raw_survey_with_references

def write_outline(topic, model, section_num, outline_reference_num, db, api_key, api_url, paper_provider=None, organization_id=None):
    outline_writer = outlineWriter(model=model, api_key=api_key, api_url = api_url, database=db, paper_provider=paper_provider, organization_id=organization_id)
    print(outline_writer.api_model.chat('hello'))
    outline = outline_writer.draft_outline(topic, outline_reference_num, 30000, section_num)
    return outline, remove_descriptions(outline)

def write_subsection(topic, model, outline, subsection_len, rag_num, db, api_key, api_url, paper_provider=None, organization_id=None, refinement = True):

    subsection_writer = subsectionWriter(model=model, api_key=api_key, api_url = api_url, database=db, paper_provider=paper_provider, organization_id=organization_id)
    if refinement:
        raw_survey, raw_survey_with_references, raw_references, refined_survey, refined_survey_with_references, refined_references = subsection_writer.write(topic, outline, subsection_len = subsection_len, rag_num = rag_num, refining = True)
        return raw_survey, raw_survey_with_references, raw_references, refined_survey, refined_survey_with_references, refined_references
    else:
        raw_survey, raw_survey_with_references, raw_references = subsection_writer.write(topic, outline, subsection_len = subsection_len, rag_num = rag_num, refining = False)
        return raw_survey, raw_survey_with_references, raw_references

def paras_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--gpu',default='0', type=str, help='Specify the GPU to use')
    parser.add_argument('--saving_path',default='./output/', type=str, help='Directory to save the output survey')
    parser.add_argument('--model',default='gpt-4o-2024-05-13', type=str, help='Model to use')
    parser.add_argument('--topic',default='', type=str, help='Topic to generate survey for')
    parser.add_argument('--section_num',default=7, type=int, help='Number of sections in the outline')
    parser.add_argument('--subsection_len',default=700, type=int, help='Length of each subsection')
    parser.add_argument('--outline_reference_num',default=1500, type=int, help='Number of references for outline generation')
    parser.add_argument('--rag_num',default=60, type=int, help='Number of references to use for RAG')
    parser.add_argument('--api_url',default='https://api.openai.com/v1/chat/completions', type=str, help='url for API request')
    parser.add_argument('--api_key',default='', type=str, help='API key for the model')
    parser.add_argument('--organization_id',default='', type=str, help='OpenAI organization ID (optional)')
    parser.add_argument('--db_path',default='./database', type=str, help='Directory of the database.')
    parser.add_argument('--embedding_model',default='nomic-ai/nomic-embed-text-v1', type=str, help='Embedding model for retrieval.')
    parser.add_argument('--paper_json_path',default='', type=str, help='Path to JSON file containing pre-selected papers (optional)')
    args = parser.parse_args()
    return args

def main(args):

    db = database(db_path = args.db_path, embedding_model = args.embedding_model)
    
    # 初始化paper provider（如果提供了JSON文件路径）
    paper_provider = None
    if hasattr(args, 'paper_json_path') and args.paper_json_path:
        try:
            paper_provider = PaperProvider(args.paper_json_path)
            print(f"Using paper provider with {len(paper_provider.papers)} papers")
        except Exception as e:
            print(f"Warning: Failed to load paper provider: {e}")
            print("Falling back to database-based retrieval")
    
    api_key = args.api_key

    if not os.path.exists(args.saving_path):
        os.mkdir(args.saving_path)

    outline_with_description, outline_wo_description = write_outline(args.topic, args.model, args.section_num, args.outline_reference_num, db, args.api_key, args.api_url, paper_provider, args.organization_id)

    raw_survey, raw_survey_with_references, raw_references, refined_survey, refined_survey_with_references, refined_references = write_subsection(args.topic, args.model, outline_with_description, args.subsection_len, args.rag_num, db, args.api_key, args.api_url, paper_provider, args.organization_id)

    with open(f'{args.saving_path}/{args.topic}.md', 'a+') as f:
        f.write(refined_survey_with_references)
    with open(f'{args.saving_path}/{args.topic}.json', 'a+') as f:
        save_dic = {}
        save_dic['survey'] = refined_survey_with_references
        save_dic['reference'] = refined_references
        f.write(json.dumps(save_dic, indent=4))

if __name__ == '__main__':

    args = paras_args()

    main(args)