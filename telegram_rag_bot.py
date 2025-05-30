import os
import re
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

from langchain_community.document_loaders.github import GithubFileLoader
from alith import Agent, MilvusStore, chunk_text

# --------------------------------------------
# Load secrets
# --------------------------------------------
load_dotenv()
GITHUB_ACCESS_KEY = os.getenv("GITHUB_ACCESS_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --------------------------------------------
# Config
# --------------------------------------------
GITHUB_REPO = "0xLazAI/alith"
DOC_RELATIVE_PATH = "website/src/content"

logging.getLogger("alith").setLevel(logging.ERROR)

# --------------------------------------------
# Step 1: Load + chunk + store
# --------------------------------------------
def create_vector_store():
    print("📥 Fetching docs from GitHub...")
    docs = GithubFileLoader(
        repo=GITHUB_REPO,
        access_token=GITHUB_ACCESS_KEY,
        github_api_url="https://api.github.com",
        file_filter=lambda path: re.match(f"{DOC_RELATIVE_PATH}/.*\\.mdx?", path),
    ).load()

    chunks = []
    for doc in docs:
        try:
            chunks.extend(chunk_text(doc.page_content, overlap_percent=0.2, max_chunk_token_size=512))
        except Exception as e:
            print("⚠️ Chunking failed:", e)

    print(f"✅ Stored {len(chunks)} chunks.")

    # ✅ Write chunks to file for manual verification
    with open("embedded_chunks.txt", "w") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"\n--- Chunk {i + 1} ---\n{chunk}\n")

    return MilvusStore().save_docs(chunks)

vector_store = create_vector_store()

# --------------------------------------------
# Step 2: Alith Agent (GPT-4 + Metis style)
# --------------------------------------------
agent = Agent(
    name="MetisRAGBot",
    model="gpt-4",
    preamble="""
You are a helpful assistant from the Metis L2 ecosystem.
onchain references, and explain concepts clearly.
""",
    store=vector_store,
)

# --------------------------------------------
# Step 3: Telegram handler
# --------------------------------------------
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    response = agent.prompt(user_input)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# async def handle_message(update: Update, context: CallbackContext) -> None:
#     user_input = update.message.text
#     print(f"\n🧠 User asked: {user_input}")

#     # Retrieve top relevant chunks manually
#     retrieved_chunks = vector_store.similarity_search(user_input, k=5)

#     print("\n📚 Retrieved chunks (shown in terminal):")
#     for i, chunk in enumerate(retrieved_chunks):
#         preview = chunk.page_content[:250].replace("\n", " ")
#         print(f"\n--- Chunk {i + 1} ---\n{preview}")

#     # Ask Alith agent
#     response = agent.prompt(user_input)
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# --------------------------------------------
# Step 4: Run Telegram bot
# --------------------------------------------
def main():
    print("🚀 Starting Metis x LazAI Telegram RAG Bot...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()