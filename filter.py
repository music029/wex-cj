import json
import urllib.request


# 原始接口地址
SOURCE = "https://你的源地址/fish.json"


CONFIG_FILE = "config.json"

OUTPUT_FILE = "fish.json"



def load_json(file):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_json(file, data):

    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )



def fetch_source():

    req = urllib.request.Request(
        SOURCE,
        headers={
            "User-Agent":
            "Mozilla/5.0"
        }
    )


    with urllib.request.urlopen(
        req,
        timeout=20
    ) as response:

        return json.loads(
            response.read()
            .decode("utf-8")
        )



def main():

    print("开始获取源接口...")


    cfg = load_json(
        CONFIG_FILE
    )


    data = fetch_source()



    order = cfg["sites_order"]

    rename = cfg["rename"]



    source_sites = data.get(
        "sites",
        []
    )



    temp = {}



    # 白名单过滤
    for site in source_sites:


        key = site.get(
            "key"
        )


        if key in order:


            # 修改名称

            if key in rename:

                site["name"] = rename[key]


            temp[key] = site




    # 按指定顺序输出

    sites = []


    for key in order:


        if key in temp:

            sites.append(
                temp[key]
            )




    result = {

        "spider":
        data.get(
            "spider",
            ""
        ),


        "wallpaper":
        data.get(
            "wallpaper",
            ""
        ),


        "logo":
        data.get(
            "logo",
            ""
        ),


        "sites":
        sites

    }



    save_json(
        OUTPUT_FILE,
        result
    )



    print(
        "采集站点生成完成"
    )


    print(
        "数量:",
        len(sites)
    )


    for s in sites:

        print(
            s.get("name")
        )



if __name__ == "__main__":

    main()
