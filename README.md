# Static Site Generator in python

### Functions in `src/util.py`

- `split_nodes_delimiter`:
    args: 
        - old_nodes: list[TextNode]
        - delimiter: str
        - text_type: TextType

    returns: list[TextNode]

- `extract_markdown_images`:
    args:
        - text: str

    returns: list[tuple]

- `extract_markdown_images`:
    args:
        - text: str

    returns: list[tuple]

- `split_nodes_image`:
    args:
        - old_nodes: list[TextNode]

    returns: list[TextNode]

- `split_nodes_link`:
    args:
        - old_nodes: list[TextNode]

    returns: list[TextNode]

- `text_to_textnodes`:
    args:
        - text: str

    returns: list[TextNode]

- `markdown_to_blocks`:
    args:
        - markdown: str
        
    returns: list[str]
