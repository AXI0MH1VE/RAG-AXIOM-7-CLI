
import click
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from bs4 import BeautifulSoup

def load_and_parse_knowledge(url):
    """Fetches content from a URL and parses it into clean sentences."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        # Use BeautifulSoup to get clean text
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs])
        # Split into sentences using a more robust regex
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
        # Filter out short/empty sentences
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        return sentences
    except requests.exceptions.RequestException as e:
        click.echo(f"Error fetching URL: {e}", err=True)
        return None

def retrieve_context(query, corpus, vectorizer, tfidf_matrix, top_k=3):
    """Retrieves the top_k most relevant sentences from the corpus."""
    query_tfidf = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_tfidf, tfidf_matrix).flatten()
    # Get the indices of the top_k most similar sentences
    relevant_indices = np.argsort(cosine_similarities)[-top_k:][::-1]
    return [corpus[i] for i in relevant_indices]

def deterministic_generator_stub(query, context):
    """A deterministic stub for the generation part of RAG."""
    if not context:
        return "I couldn't find any relevant information to answer that question.", []

    response = f"Based on the retrieved context, here is an answer to '{query}':\n"
    response += "..." # A simple generative-like lead-in
    
    cited_context = []
    for i, sentence in enumerate(context):
        response += f"\n\n\"{sentence}\""
        cited_context.append(sentence)
        
    return response, cited_context

@click.command()
@click.argument('url', default='https://en.wikipedia.org/wiki/Artificial_intelligence')
def main(url):
    """
    Nexus RAG Engine: A groundbreaking AI tool for live knowledge retrieval.
    
    Ingests knowledge from a URL and answers questions based on it.
    """
    click.echo(f"Initializing Nexus Engine. Ingesting knowledge from: {url}")
    corpus = load_and_parse_knowledge(url)
    
    if not corpus:
        click.echo("Failed to load knowledge base. Exiting.")
        return

    click.echo(f"Knowledge base ingested successfully. ({len(corpus)} sentences)")
    
    # Vectorize the corpus
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(corpus)
    click.echo("Semantic vectorization complete. Ready for queries.")
    
    click.echo("\n--- Nexus Interactive Mode ---")
    click.echo("Ask a question, or type 'exit' to quit.")
    
    while True:
        query = click.prompt(">")
        if query.lower() == 'exit':
            break
            
        # 1. Retrieve
        context = retrieve_context(query, corpus, vectorizer, tfidf_matrix)
        
        # 2. Generate (stub)
        answer, citations = deterministic_generator_stub(query, context)
        
        click.echo("\n" + "="*20 + " NEXUS RESPONSE " + "="*20)
        click.echo(answer)
        click.echo("-"*(40 + 18))
        click.echo("Citations:")
        for i, citation in enumerate(citations):
            click.echo(f"  [{i+1}] {citation[:80]}...")
        click.echo("="*(40 + 18) + "\n")

if __name__ == '__main__':
    main()
