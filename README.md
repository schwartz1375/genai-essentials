# GenAI Essentials

A collection of Jupyter notebooks covering essential concepts in Generative AI and Large Language Models.

## Getting Started

1. Install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  
   pip install -r requirements.txt
   ```

2. Work through the notebooks in this order:

   1. **[llm_security.ipynb](llm_security.ipynb)** - Security considerations and best practices for LLMs
   2. **[llm_tutorial.ipynb](llm_tutorial.ipynb)** - Core LLM concepts and basic agent introduction
   3. **[local_rag.ipynb](local_rag.ipynb)** - Retrieval-Augmented Generation with local data
   4. **[multimodal_llms.ipynb](multimodal_llms.ipynb)** - Vision-language models and document understanding
   5. **[agent_frameworks.ipynb](agent_frameworks.ipynb)** - Deep dive into agent patterns and architectures
   6. **[mcp_integration/](mcp_integration/)** - Model Context Protocol for AI tool integration

## Learning Progression

The notebooks build on each other:
- **Tutorial** introduces agents with simple examples (taste/intro)
- **RAG** shows document-based retrieval and vector databases
- **Agent Frameworks** explores advanced patterns in depth (ReAct, Plan-Execute, Multi-agent) and includes RAG-enabled agents
- **Multimodal** demonstrates vision-enabled agents
- **MCP Integration** shows how to extend AI assistants with custom tools and security capabilities

## Directory Structure

- `./data/` - Sample documents used for RAG demonstrations
  - `./data/markdowns/` - Content from https://github.com/notaspork/linuxexamples/tree/main/basic
- `./temp/` - Working directory for temporary files (created at runtime)
- `./chroma_llm_training/` - Vector database created by llm_tutorial.ipynb (generated at runtime)
- `./chromadb_store/` - Vector database created by local_rag.ipynb (generated at runtime)
- `./chroma_agents/` - Vector database created by agent_frameworks.ipynb (generated at runtime)
- `./mcp_integration/` - Model Context Protocol servers and configurations

## Prerequisites

- Python 3.8+
- Jupyter Notebook or JupyterLab

## Additional Resources

- **[Prompt Engineering Guide](https://www.promptingguide.ai/)** - Comprehensive guide to effective prompting techniques
- **[Ollama Models](https://ollama.ai/library)** - Local model library for privacy-focused development

## License

See [LICENSE](LICENSE) file for details.
