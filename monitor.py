import os
import json
import requests
from datetime import datetime


CONFIG_FILE = "config.json"
VERSION_FILE = "versions.json"
CHANGELOG_FILE = "CHANGELOG.md"


# =========================
# JSON 操作
# =========================


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



# =========================
# 获取 GitHub Release
# =========================


def get_latest_release(repo):

    url = (
        f"https://api.github.com/"
        f"repos/{repo}/releases/latest"
    )


    response = requests.get(
        url,
        timeout=10
    )


    if response.status_code != 200:

        print(
            "获取失败:",
            repo,
            response.text
        )

        return None



    data = response.json()


    return {

        "version":
            data.get(
                "tag_name",
                "unknown"
            ),

        "title":
            data.get(
                "name",
                ""
            ),

        "body":
            data.get(
                "body",
                ""
            ),

        "url":
            data.get(
                "html_url",
                ""
            )

    }



# =========================
# 生成单独更新文件
# =========================


def create_update_markdown(
        name,
        release
):

    folder = (
        "updates/"
        +
        name.lower()
    )


    os.makedirs(
        folder,
        exist_ok=True
    )


    date = datetime.now().strftime(
        "%Y-%m-%d"
    )


    filename = (
        folder
        +
        "/"
        +
        date
        +
        "-"
        +
        release["version"]
        +
        ".md"
    )


    content = f"""# {name} 更新记录


## 版本

{release['version']}


## 发布时间

{date}


## Release

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



    print(
        "生成:",
        filename
    )



# =========================
# 更新 CHANGELOG
# =========================


def update_changelog(
        name,
        release
):

    date = datetime.now().strftime(
        "%Y-%m-%d"
    )


    new_log = f"""

## {name}


### {release['version']}


发布时间:

{date}


Release:

{release['url']}


更新内容:

{release['body']}


---

"""


    old_content = ""


    if os.path.exists(
        CHANGELOG_FILE
    ):

        with open(
            CHANGELOG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            old_content = f.read()



    header = (
        "# Endstone / LeviLamina 更新日志\n\n"
    )


    if old_content.startswith(
        header
    ):

        old_content = old_content[
            len(header):
        ]



    with open(
        CHANGELOG_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            header
            +
            new_log
            +
            old_content
        )


    print(
        "更新 CHANGELOG"
    )



# =========================
# 主程序
# =========================


def main():

    config = load_json(
        CONFIG_FILE
    )


    versions = load_json(
        VERSION_FILE
    )


    changed = False



    for item in config["repositories"]:


        name = item["name"]

        repo = item["repo"]



        release = get_latest_release(
            repo
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



        # 没更新

        if old_version == new_version:

            print(
                "无更新"
            )

            continue



        print(
            "发现新版本!"
        )


        create_update_markdown(
            name,
            release
        )


        update_changelog(
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

        print(
            "版本记录已保存"
        )


    else:

        print(
            "没有任何变化"
        )



if __name__ == "__main__":

    main()
