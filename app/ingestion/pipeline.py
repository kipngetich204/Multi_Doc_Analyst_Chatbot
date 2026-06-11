from app.ingestion.loader.loader import DocumentLoader
class Pipeline:

    @staticmethod
    def build_pipeline():
        """Main execution function to batch ingest the target directory."""
        target_dir = "data"
        print(f"Starting ingestion for directory: '{target_dir}'...")
        
        documents = DocumentLoader.load_directory(target_dir)
        
        print(f"\nSuccessfully loaded {len(documents)} document chunk(s).")
        
        # Showcase content snippets to verify ingestion success
        for i, doc in enumerate(documents[:3]):
            source = doc.metadata.get("source", "Unknown")
            snippet = doc.page_content[:100].replace('\n', ' ')
            print(f"Doc {i+1} | Source: {source} | Snippet: {snippet}...")
            
        return documents