import json
import urllib.request


# ==========================
# 源接口地址
# 修改成你的原始 fish.json 地址
# ==========================

SOURCE = "https://9280.kstore.vip/aiwex.json"


# 输出文件

CONFIG_FILE = "config.json"

OUTPUT_FILE = "fish.json"



# ==========================
# 读取配置
# ==========================

def load_json(file):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



# ==========================
# 保存文件
# ==========================

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



# ==========================
# 获取源接口
# ==========================

def fetch_source():

    req = urllib.request.Request(

        SOURCE,

        headers={

            # 必须英文
            "User-Agent":
            "Mozilla/5.0"

        }

    )


    try:

        with urllib.request.urlopen(

            req,

            timeout=30

        ) as response:


            text = response.read().decode(

                "utf-8"

            )


            return json.loads(text)



    except Exception as e:


        print(

            "获取源接口失败:",

            e

        )


        raise



# ==========================
# 主程序
# ==========================

def main():


    print(
        "开始获取源接口..."
    )



    cfg = load_json(

        CONFIG_FILE

    )



    data = fetch_source()



    order = cfg.get(

        "sites_order",

        []

    )



    rename = cfg.get(

        "rename",

        {}

    )



    source_sites = data.get(

        "sites",

        []

    )



    temp = {}



    # ======================
    # 白名单过滤
    # ======================

    for site in source_sites:


        key = site.get(

            "key"

        )



        if key in order:


            # 修改名称

            if key in rename:

                site["name"] = rename[key]



            temp[key] = site




    # ======================
    # 按指定顺序输出
    # ======================

    sites = []



    for key in order:


        if key in temp:


            sites.append(

                temp[key]

            )




    # ======================
    # 生成结果
    # ======================

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




    print()

    print(

        "===================="

    )


    print(

        "采集站点生成完成"

    )


    print(

        "数量:",

        len(sites)

    )


    print(

        "===================="

    )


    for s in sites:


        print(

            s.get(

                "name",

                ""

            )

        )





if __name__ == "__main__":


    main()
