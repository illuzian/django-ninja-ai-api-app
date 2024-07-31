from langchain_community.document_transformers import Html2TextTransformer
import html2text


def transform_document(document: str) -> str:
    # print(document)
    return html2text.html2text(document)



