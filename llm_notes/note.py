from pathlib import Path
import re
from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from typing import List, Optional
import yaml
import networkx as nx



class NoteMetadata(BaseModel):
    title: str
    tags: List[str] = []
    note_links: List[str] = []
    back_links: List[str] = []
    short_title: str = ""


@dataclass
class Note:
    path: Path
    title: str  # includes extension
    full_text: str
    lines: List[str]
    tags: List[str]
    sources: List[str]  # url
    urls: List[str]
    body: str
    metadata: NoteMetadata

    def __str__(self):
        return f"{self.title=}, {self.tags=}, {self.sources=}"


def load(file_path: Path):
    with open(file_path, "r") as f:
        title = file_path.stem
        full_text = "\n".join([title,f.read()])
        f.seek(0, 0)
        lines = [line.rstrip() for line in f]
        tags = re.findall("\#\w+", full_text)
        urls = re.findall("https?://(?:[-\w./?=]|(?:%[\da-fA-F]{2}))+", full_text)
        source_lines = [l for l in lines if "source" in l]
        sources = (
            re.findall("https?://(?:[-\w./?=]|(?:%[\da-fA-F]{2}))+", source_lines[0])
            if source_lines
            else []
        )
        body = "\n".join([l for l in lines if not ("source" in l or "tags" in l)])
        note_links = re.findall("\[\[(.*?)\]\]", full_text)
        short_title = shorten_title(file_path.name)
        base_metadata = NoteMetadata(
            title=file_path.name,
            tags=tags,
            note_links=note_links,
            short_title=short_title,
        )

        return Note(
            path=file_path,
            title=title,
            full_text=full_text,
            lines=lines,
            tags=[] if tags is None else tags,
            sources=sources,
            urls=urls,
            body=body,
            metadata=base_metadata,
        )


def shorten_title(title: str, word_length=5) -> str:
    # Define a list of articles to strip
    articles = [
        "a",
        "an",
        "the",
        "of",
        "for",
        "and",
        "but",
        "or",
        "nor",
        "on",
        "at",
        "to",
        "from",
        "by",
        "as",
        "in",
        "with",
    ]
    # Remove leading/trailing whitespaces
    title = title.strip()
    # Convert to lowercase
    title = title.lower()
    # Split the title into words
    words = title.split()
    # Remove articles from the list of words
    words = [word for word in words if word not in articles]
    # remove vowels if they are in the middle of the word
    words = [
        re.sub(r"(?<!^)[aeiouAEIOU](?!$)", "", word)
        if len(word) > word_length
        else word
        for word in words
    ]
    # Shorten words to five letters
    words = [word[:word_length] for word in words]
    # Join the words with underscores
    shortened_title = "_".join(words)

    return shortened_title


def load_note_directory(path: Path):
    file_paths = path.glob("*.md")
    notes = [load(fp) for i, fp in enumerate(file_paths)]
    return notes


def write_note(path, lines):
    with open(path, "w") as f:
        f.writelines(lines)


def construct_full_text(lines, metadata):
    return "".join(
        [
            "---\n",
            yaml.dump(metadata),
            "---\n\n",
            "\n".join(lines),
        ]
    )


def construct_note_graph(notes: list[Note]) -> nx.Graph:
    short_lookup = {}
    title_edges = {}
    
    for note in notes:
        if note.metadata is not None:
            short_title = short_lookup.setdefault(note.title, shorten_title(note.title))
            title_edges[short_title] = [
                short_lookup.setdefault(link, shorten_title(link))
                for link in note.metadata.note_links
            ]
    graph = nx.from_dict_of_lists(
        {
            n.metadata.short_title: [
                shorten_title(link_title) for link_title in n.metadata.note_links
            ]
            for n in notes if n.metadata is not None
        }
    )
    return graph


if __name__ == "__main__":
    path = Path("../zettelkasten/docs/public_zettels/")
    for i, n in enumerate(load_note_directory(path)):
        print(i, n)
