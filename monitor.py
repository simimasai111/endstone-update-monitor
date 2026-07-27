import os
import json
import requests
from datetime import datetime


CONFIG = "config.json"
VERSION_FILE = "versions.json"


def load_json(path):

    if not os.path.exists(path):
        return {}

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)



def save_json(path, data):

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )



def get_release(repo):

    url = (
        f"https://api.github.com/"
        f"repos/{repo}/releases/latest"
    )

    r = requests.get(url)


    if r.status_code != 200:
        return None


    data = r.json()


    return {

        "version": data["tag_name"],

        "title": data["name"],

        "body": data["body"] or "",

        "url": data["html_url"]

    }



def create_markdown(
        name,
        release
):

    folder = (
        "updates/"
        + name.lower()
    )


    os.makedirs(
        folder,
        exist_ok=True
    )


    filename = (
        folder
        + "/"
        + datetime.now()
        .strftime("%Y-%m-%d")
        + "-"
        + release["version"]
        + ".md"
    )


    content = f"""
# {name} 更新记录


## 版本

{release['version']}


## 发布标题

{release['title']}


## 更新时间

{datetime.now().strftime("%Y-%m-%d")}


## GitHub

{release['url']}


## 更新内容

{release['body']}

"""


    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(content)



def main():

    config = load_json(CONFIG)

    versions = load_json(VERSION_FILE)


    changed = False


    for repo in config["repositories"]:

        name = repo["name"]


        release = get_release(
            repo["repo"]
        )


        if not release:
            continue


        old_version = versions.get(
            name
        )


        new_version = release["version"]


        print(
            f"{name}: {old_version} -> {new_version}"
        )


        # 版本一致，跳过

        if old_version == new_version:

            print(
                "没有更新"
            )

            continue



        # 新版本

        print(
            "发现新版本"
        )


        create_markdown(
            name,
            release
        )


        versions[name] = new_version


        changed = True



    if changed:

        save_json(
            VERSION_FILE,
            versions
        )


if __name__ == "__main__":
    main()
