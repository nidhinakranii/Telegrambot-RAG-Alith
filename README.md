# Metis x LazAI Telegram RAG Bot

This project demonstrates how to build an intelligent Telegram chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions about the Alith framework. It fetches documentation from a GitHub repo, embeds it into a Milvus vector database, and uses GPT-4 to provide context-aware responses—all from inside Telegram.

## Features

- **Real-time Documentation Retrieval**: Fetches live docs from Alith GitHub repository  
- **Intelligent Question Answering**: Uses GPT-4 with RAG for context-aware responses  
- **Vector Database Storage**: Utilizes Milvus for efficient document embedding storage  
- **Telegram Integration**: Seamless chat interface through Telegram Bot API  
- **Chunk-based Processing**: Optimized document processing for better retrieval  

## What is Retrieval-Augmented Generation (RAG)?

RAG is a powerful method that improves the quality of AI-generated responses by combining a language model with a retrieval system. Instead of relying solely on model memory, the system retrieves relevant documents from a knowledge base and uses that context for generation. In this project, we use the Alith SDK with Milvus as the vector store and GPT-4 as the model.

This architecture helps Alith developers and Metis community members to interact with their documentation in real-time using natural language.

## Prerequisites

Before you begin, ensure you have:

- Python 3.10 or higher
- A GitHub personal access token
- A Telegram bot token (from BotFather)
- An OpenAI API key (for GPT-4)
- Basic understanding of AI agents and vector search
- A Metis L2 ecosystem interest (optional but useful)

## Installation

### Step 1: Set Up Your Project Directory

```bash
mkdir telegram-rag-bot && cd telegram-rag-bot
```

### Step 2: Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### Step 3: Install Required Libraries

```bash
pip install alith
pip install python-telegram-bot
pip install langchain-community
pip install -U pymilvus["model"]
```

### Step 4: Set Environment Variables

Create a `.env` file in your root directory:

```env
GITHUB_ACCESS_KEY=your-github-token
OPENAI_API_KEY=your-openai-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

Then load it:

```bash
export $(cat .env | xargs)
```

## Step 5: Write the Bot Code

Create a Python file called `telegram_rag_bot.py` and paste the full bot code you have developed.

> It includes GitHub doc loader, chunking via `chunk_text()`, Milvus storage, and Telegram interaction.

## Step 6: Run the Bot

Make sure your virtual environment is activated, then run:

```bash
python telegram_rag_bot.py
```

You should see logs like:

```
📥 Fetching docs from GitHub...
✅ Stored 76 chunks.
Starting Metis x LazAI Telegram RAG Bot...
```

Now open your Telegram app and chat with your bot.

## Project Structure

```
telegram-rag-bot/
├── telegram_rag_bot.py         # Main bot script
├── .env                        # Your API keys
├── embedded_chunks.txt         # Saved chunks for verification
├── venv/                       # Python virtual environment
└── README.md                   # Documentation
```

## Usage

Once the bot is running, go to Telegram and message your bot like:

- What is Alith?
- What is Chain of Thought?
- How does RAG work in Alith?

The bot retrieves relevant chunks from GitHub docs and answers via GPT-4.

## Testing and Verification

- **Log inspection**: You can check the `embedded_chunks.txt` file to view all processed document chunks.
- **Chunk matching**: Match Telegram answers with the content from `embedded_chunks.txt` to confirm retrieval.
- **Manual query**: You can use `vector_store.similarity_search("your query")` in Python for chunk inspection.

## Troubleshooting

### Common Issues

- **Bot not responding**: Make sure your `.env` keys are correct and `.env` is sourced.
- **No chunks stored**: Check GitHub repo path and access token.
- **Vector store not found**: Ensure `MilvusLite` or `pymilvus` is installed correctly.

### Debugging Tips

- Add print statements after chunking or retrieval
- Check Telegram logs in terminal
- Use `print(response)` inside the message handler to trace outputs

## Resources

- [Alith Documentation](https://alith.lazai.network/docs)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Milvus Vector DB](https://milvus.io/)
- [OpenAI GPT-4](https://platform.openai.com/)
- [Metis L2 Docs](https://docs.metis.io)

## Contributing

We welcome contributions! Please:

- Fork this repository (if open-sourced later)
- Create a new feature branch
- Submit a pull request
- Write meaningful commits and comments

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Conclusion

You’ve now built a fully functional AI Telegram bot powered by Alith, GPT-4, and Milvus. This bot can intelligently respond to queries using live documentation context. Next, consider exploring how to use this same RAG pipeline with custom data or integrate with Alith's on-chain agents or workflows.
