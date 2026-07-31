from gpt4all import GPT4All
from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Load GPT4All Model (CPU)
model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf", device="cpu")

# Load Sentence Transformer for semantic similarity
semantic_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load NIC Data
file_path = "NIC_5digit.csv"
df = pd.read_csv(file_path)

# Encode NIC descriptions for fast similarity search
df["Embeddings"] = df["NIC description"].apply(lambda x: semantic_model.encode(x, convert_to_tensor=True))


def refine_query(details):
    """Refine user query into a structured format using GPT-4All"""
    prompt = f"Convert the following business description into a structured search query: {details}"
    response = model.generate(prompt, max_tokens=50)
    return response.strip()


def get_nic_code(details, df, top_n=5):
    """Find the most relevant NIC codes using semantic similarity"""
    refined_query = refine_query(details)
    query_embedding = semantic_model.encode(refined_query, convert_to_tensor=True)

    # Compute similarity scores
    df["Similarity"] = df["Embeddings"].apply(lambda x: util.pytorch_cos_sim(query_embedding, x).item())

    # Sort and get top matches
    top_matches = df.nlargest(top_n, "Similarity")[["NICcode", "NIC description"]]

    return top_matches.to_dict(orient="records")

from deep_translator import GoogleTranslator
def translate_to_english(text):
    return GoogleTranslator(source='auto', target='en').translate(text)

input = "company using IT Sector for healthservices"
translated = translate_to_english(input)
# Example Test
print(get_nic_code(translated, df))
