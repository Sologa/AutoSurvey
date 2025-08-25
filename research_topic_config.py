"""
基于研究配置的survey主题配置
"""

RESEARCH_TOPIC = """
Large Language Models (LLMs) in Academic Research Applications: A Comprehensive Survey

This survey focuses on the intersection of Large Language Models and academic research workflows, 
covering automated literature review, AI-assisted academic writing, research automation, 
and the development of research tools and frameworks. The scope includes:

Primary Areas:
- LLMs in academic research applications and workflows
- Automated literature review and systematic review generation
- AI-assisted academic writing and research assistance
- Natural Language Processing applications in academic domains

Key Technologies:
- LLM agents and research assistants
- Automation in academic research processes
- Survey and review generation with AI
- Research workflow automation frameworks

Application Domains:
- Computer Science and AI research
- Information retrieval and digital libraries
- Software engineering and human-computer interaction
- Medical/health informatics and education technology
- Quantitative biology and library science

This survey aims to provide a comprehensive overview of how LLMs are transforming 
academic research practices, from literature discovery to automated report generation, 
while examining the practical applications, methodologies, and frameworks that enable 
researchers to leverage AI for enhanced productivity and research quality.
"""

# 从研究配置中提取的关键词组合
KEYWORD_COMBINATIONS = [
    "LLM survey automation",
    "LLM research assistant", 
    "AutoSurvey and related tools",
    "Agent laboratory research",
    "Research tool frameworks",
    "Writing generation systems"
]

# 研究领域要求
FIELD_REQUIREMENTS = [
    "Computer Science (cs.*)",
    "Artificial Intelligence (cs.AI)", 
    "Computation and Language (cs.CL)",
    "Software Engineering (cs.SE)",
    "Information Retrieval (cs.IR)",
    "Human–Computer Interaction (cs.HC)",
    "Digital Libraries (cs.DL)",
    "Information Systems (cs.IS)",
    "Computers and Society (cs.CY)",
    "Machine Learning (stat.ML)",
    "Quantitative Biology (q-bio.QM)",
    "Library and Information Science (LIS)",
    "Medical/Health Informatics",
    "Education Technology / Learning Sciences"
]

def get_research_topic():
    """获取研究主题描述"""
    return RESEARCH_TOPIC.strip()

def get_keyword_combinations():
    """获取关键词组合"""
    return KEYWORD_COMBINATIONS

def get_field_requirements():
    """获取研究领域要求"""
    return FIELD_REQUIREMENTS
