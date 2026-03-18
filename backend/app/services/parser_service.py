from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader


def extract_text(file_path: str, ext: str, max_chars: int = 12000) -> str:
    """
    Extracts and cleans text from PDF or DOCX using LangChain loaders.

    Args:
        file_path (str): Path to the uploaded file
        ext (str): File extension (.pdf or .docx)
        max_chars (int): Max characters to keep (to control token size)

    Returns:
        str: Cleaned text ready for LLM
    """

    try:
        # Select loader
        if ext.lower() == ".pdf":
            loader = PyPDFLoader(file_path)

        elif ext.lower() == ".docx":
            loader = Docx2txtLoader(file_path)

        else:
            raise ValueError("Unsupported file type")

        # Load documents
        documents = loader.load()

        if not documents:
            raise ValueError("No content extracted from document")

        # Combine pages
        full_text = "\n".join(
            [doc.page_content for doc in documents if doc.page_content]
        )

        # Basic cleaning
        full_text = full_text.replace("\n\n", "\n").strip()

        if not full_text:
            raise ValueError("Extracted text is empty")

        # 🔥 IMPORTANT: Limit size (LLM safety)
        if len(full_text) > max_chars:
            full_text = full_text[:max_chars]

        return full_text

    except Exception as e:
        raise RuntimeError(f"Parsing failed: {str(e)}")