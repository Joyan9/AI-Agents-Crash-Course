import io
import zipfile
import requests
import frontmatter
from minsearch import Index


def read_repo_data(repo_owner, repo_name):
    url = f"https://codeload.github.com/{repo_owner}/{repo_name}/zip/refs/heads/main"
    resp = requests.get(url)
    resp.raise_for_status()

    repository_data = []
    zf = zipfile.ZipFile(io.BytesIO(resp.content))

    for file_info in zf.infolist():
        filename = file_info.filename.lower()
        if not (filename.endswith(".md") or filename.endswith(".mdx")):
            continue

        with zf.open(file_info) as f_in:
            content = f_in.read()
            post = frontmatter.loads(content)
            data = post.to_dict()

            # Strip the top-level zip folder prefix so filenames are clean
            _, filename_repo = file_info.filename.split("/", maxsplit=1)
            data["filename"] = filename_repo
            repository_data.append(data)

    zf.close()
    return repository_data


def index_data(repo_owner, repo_name):
    docs = read_repo_data(repo_owner, repo_name)

    # Drop any docs with empty filenames (e.g. root-level zip entry)
    docs = [d for d in docs if d.get("filename")]

    index = Index(text_fields=["content", "filename"])
    index.fit(docs)
    return index