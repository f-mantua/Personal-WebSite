import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime

WXR_PATH = r"C:\Users\feder\Downloads\federicomantua.WordPress.2026-02-08.xml"
OUTPUT_ROOT = r"C:\Personal\Blog\content"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\s-]", "", value)
    value = re.sub(r"[\s-]+", "-", value)
    return value or "post"


def to_iso(dt_str: str) -> str:
    if not dt_str:
        return ""
    try:
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return dt_str


def collect_terms(item):
    tags = []
    categories = []
    for cat in item.findall("category"):
        domain = cat.get("domain", "")
        name = (cat.text or "").strip()
        if not name:
            continue
        if domain == "post_tag":
            tags.append(name)
        elif domain == "category":
            categories.append(name)
    return tags, categories


def write_markdown(path, front_matter, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n")
        for key, value in front_matter.items():
            if value is None or value == "":
                continue
            if isinstance(value, bool):
                f.write(f"{key}: {'true' if value else 'false'}\n")
            elif isinstance(value, list):
                if not value:
                    continue
                f.write(f"{key}:\n")
                for v in value:
                    f.write(f"  - {v}\n")
            else:
                f.write(f"{key}: {value}\n")
        f.write("---\n\n")
        f.write(body.strip())
        f.write("\n")


def main():
    ns = {}
    for event, elem in ET.iterparse(WXR_PATH, events=("start-ns",)):
        ns[elem[0]] = elem[1]

    tree = ET.parse(WXR_PATH)
    root = tree.getroot()

    wp_ns = ns.get("wp")
    content_ns = ns.get("content")

    post_count = 0
    page_count = 0

    for item in root.findall(".//item"):
        post_type = item.findtext(f"{{{wp_ns}}}post_type", default="")
        status = item.findtext(f"{{{wp_ns}}}status", default="")
        if post_type not in ("post", "page"):
            continue

        title = (item.findtext("title") or "Untitled").strip()
        slug = (item.findtext(f"{{{wp_ns}}}post_name") or "").strip()
        slug = slug or slugify(title)

        date = to_iso(item.findtext(f"{{{wp_ns}}}post_date", default=""))
        lastmod = to_iso(item.findtext(f"{{{wp_ns}}}post_modified", default=""))

        content = item.findtext(f"{{{content_ns}}}encoded", default="") or ""
        excerpt = item.findtext(f"{{{ns.get('excerpt')}}}encoded", default="") or ""

        tags, categories = collect_terms(item)

        draft = status != "publish"

        front_matter = {
            "title": title,
            "date": date,
            "lastmod": lastmod,
            "draft": draft,
            "slug": slug,
            "tags": tags,
            "categories": categories,
        }

        if excerpt.strip():
            front_matter["summary"] = excerpt.strip().replace("\n", " ")

        if post_type == "post":
            out_path = os.path.join(OUTPUT_ROOT, "posts", slug, "index.md")
            post_count += 1
        else:
            out_path = os.path.join(OUTPUT_ROOT, "pages", slug, "index.md")
            page_count += 1

        write_markdown(out_path, front_matter, content)

    print(f"Imported posts: {post_count}")
    print(f"Imported pages: {page_count}")


if __name__ == "__main__":
    main()
