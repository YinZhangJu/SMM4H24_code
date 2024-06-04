import os
import pandas as pd
from zhipuai import ZhipuAI
from zhipuai.core._errors import APIRequestFailedError

client = ZhipuAI(
    api_key=" "
)  # 填写您自己的APIKey


def Data_con(data_path, datas):
    for filename in os.listdir(data_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_path, filename)
            df = pd.read_csv(file_path, delimiter="\t")  # 假设是tab分隔的文本文件
            datas.append([df.columns[0]])

# 列表来存储数据框
inputresult = []
outputresult = []

Data_con("./SMM4H_2024_Task_2_test", inputresult)

from logging import getLogger, FileHandler, Formatter, DEBUG, INFO


def set_logger():
    # 全体のログ設定
    # ファイルに書き出す。ログが100KB溜まったらバックアップにして新しいファイルを作る。
    root_logger = getLogger()
    root_logger.setLevel(DEBUG)
    file_handler = FileHandler(
        r"log/glm_2step_response_for_sensitive_check.log",
        mode="a",
        encoding="utf-8",
    )
    format = Formatter("%(asctime)s : %(levelname)s : %(filename)s - %(message)s")
    file_handler.setFormatter(format)
    root_logger.addHandler(file_handler)


set_logger()
logger = getLogger(__name__)

# ログを書き込むとき
logger.debug("デバッグ用ログ")
logger.info("普通のログ")
logger.warning("やば目のログ")

model_name = "glm-3-turbo"

logger.info(f"Totally {len(inputresult)} samples to process with {model_name}.")

error_records = {"No.": [], "Sample": [], "Error Message": [], "Error Timing Step": []}

for i, list in enumerate(inputresult):

    try:
        response = client.chat.completions.create(
            model=model_name,  # 填写需要调用的模型名称
            messages=[
                {
                    "role": "user",
                    "content": "作为一名精通日法德三语的语言学家，请你找出下列日语、法语或者德语语句中的实体，尤其注意医学领域的实体，比如药物名称以及副作用等，注意简称，只提供结果，不需要推理过程\
                    举例：\
                    输入：872801880329535488:うぅ。やっぱり少し吐き気がするなぁ。レクサプロ飲みたくない。\
                    输出：{吐き気、レクサプロ}\
                    \
                    举例：\
                    输入：alut <user>, pour moi, ça a commencé à l'âge de <pi>. J'ai suivi une thérapie et une cure pendant deux ans, j'ai pris des pilules et j'ai toujours eu des angoisses avant les règles. Le gynécologue m'a fait passer des tests hormonaux, qui ont révélé une pré-ménopause. J'ai pris Kliogest après avoir pris 3 hormones différentes, ça a bien marché, mais j'ai dû arrêter parce que j'avais des saignements abondants (janvier). Changement de gynécologue qui m'a mis à une dose très faible. La situation empirait de jour en jour. Par hasard, j'ai trouvé une gynécologue très sympa qui a aussi eu de gros problèmes de ménopause. J'ai l'impression que quelqu'un me comprend. Je prends maintenant Trisequens (depuis 2 mois) et Insidon pour l'anxiété et l'humeur. Mon médecin pense qu'il me faudra encore deux mois pour retrouver mon niveau d'hormones. Je te souhaite beaucoup de force. Si tu le souhaites, tu peux m'envoyer un mail. <pi> Prends soin de toi. <user>\
                    输出：{alut、thérapie、cure、pilules、tests hormonau、pré-ménopause、Kliogest、saignements abondants、gynécologue、Trisequens、Insidon、deux mois、3 hormones différentes、angoisses、gros problèmes、anxiété、humeur}\
                    \
                    举例：\
                    输入：Hallo <user>, ich habe von September 2009 bis vor acht Wochen auch Tamoxifen genommen und die sehr gut vertragen. Klar, ich bekam Hitzewellen und habe ca. 9 kg in zwei Jahren zugenommen. Da ich aber <pi> haben sich die Kilos ganz gut verteilt. Im Gegenteil, die meisten Leute meinen, ich sähe heute besser aus als früher. Ok, bin <pi> und muss ja auch nicht mehr <pi>´s next top model werden. Jetzt nehme ich Letroblock ( Wirkstoff aus Femara ) und anfangs habe ich außer den typischen Hitzewellen nichts gemerkt. Aber seit einigen Tagen habe ich manchmal ganz fürchterliche Schmerzen in den Beinen. Ich gehe dreimal wöchentlich zum Sport, wer weiß wie es wäre, wenn ich mich kaum bewegen würde. Aber so lange ich es aushalten kann, will ich mich nicht beklagen. Was meine Haut angeht, kann ich nur sagen, dass sie sich täglich verbessert. Ich habe seit meinem 14. Lebensjahr eine chronische Psoriasis ( Schuppenflechte ) und die ist in den letzten Wochen wie von Geisterhand an manchen Stellen verschwunden. Ich wünsche Euch allen alles Liebe, <user>\
                    输出：{September 2009、vor acht Wochen、Tamoxifen、Hitzewellen、ca. 9 kg in zwei Jahren zugenommen、Letroblock、Femara 、typische Hitzewellen、Schmerzen、Beine、chronische Psoriasis、Schuppenflechte、Euch allen、Liebe、ganz fürchterliche Schmerzen}",
                },
                {
                    "role": "assistant",
                    "content": "好的，我为您筛选出了语句中的各种实体",
                },
                {"role": "user", "content": f"请找出下列{list}中的实体名称"},
            ],
        )
        str1 = response.choices[0].message
    except Exception as e:
        logger.error(f"Encounter error: {repr(e)} in first step")
        error_records["No"].append(i)
        error_records["Sample"].append(list)
        error_records["Error Message"].append(repr(e))
        error_records["Error Timing Step"].append(1)

    try:
        response = client.chat.completions.create(
            model=model_name,  # 填写需要调用的模型名称
            messages=[
                {
                    "role": "user",
                    "content": "作为一名日法德三语药剂师，请你根据前面日语、法语或者德语句子的语境，找出后面实体列表中的药物以及副作用实体，注意简称，只提供结果，不需要推理过程，注意格式用顿号划分实体\
                    举例：\
                    输入：{872801880329535488:うぅ。やっぱり少し吐き気がするなぁ。レクサプロ飲みたくない。}{吐き気、レクサプロ}\
                    输出：{药品名称：レクサプロ，副作用：吐き気}\
                    \
                    举例：\
                    输入：{alut <user>, pour moi, ça a commencé à l'âge de <pi>. J'ai suivi une thérapie et une cure pendant deux ans, j'ai pris des pilules et j'ai toujours eu des angoisses avant les règles. Le gynécologue m'a fait passer des tests hormonaux, qui ont révélé une pré-ménopause. J'ai pris Kliogest après avoir pris 3 hormones différentes, ça a bien marché, mais j'ai dû arrêter parce que j'avais des saignements abondants (janvier). Changement de gynécologue qui m'a mis à une dose très faible. La situation empirait de jour en jour. Par hasard, j'ai trouvé une gynécologue très sympa qui a aussi eu de gros problèmes de ménopause. J'ai l'impression que quelqu'un me comprend. Je prends maintenant Trisequens (depuis 2 mois) et Insidon pour l'anxiété et l'humeur. Mon médecin pense qu'il me faudra encore deux mois pour retrouver mon niveau d'hormones. Je te souhaite beaucoup de force. Si tu le souhaites, tu peux m'envoyer un mail. <pi> Prends soin de toi. <user>}{alut、thérapie、cure、pilules、tests hormonau、pré-ménopause、Kliogest、saignements abondants、gynécologue、Trisequens、Insidon、deux mois、3 hormones différentes、angoisses、gros problèmes、anxiété、humeur}\
                    输出：{药品名称：pilules、Kliogest、3 hormones différentes、Trisequens、Insidon，副作用：angoisses、saignements abondants、gros problèmes、anxiété、humeur}\
                    \
                    举例：\
                    输入：{Hallo <user>, ich habe von September 2009 bis vor acht Wochen auch Tamoxifen genommen und die sehr gut vertragen. Klar, ich bekam Hitzewellen und habe ca. 9 kg in zwei Jahren zugenommen. Da ich aber <pi> haben sich die Kilos ganz gut verteilt. Im Gegenteil, die meisten Leute meinen, ich sähe heute besser aus als früher. Ok, bin <pi> und muss ja auch nicht mehr <pi>´s next top model werden. Jetzt nehme ich Letroblock ( Wirkstoff aus Femara ) und anfangs habe ich außer den typischen Hitzewellen nichts gemerkt. Aber seit einigen Tagen habe ich manchmal ganz fürchterliche Schmerzen in den Beinen. Ich gehe dreimal wöchentlich zum Sport, wer weiß wie es wäre, wenn ich mich kaum bewegen würde. Aber so lange ich es aushalten kann, will ich mich nicht beklagen. Was meine Haut angeht, kann ich nur sagen, dass sie sich täglich verbessert. Ich habe seit meinem 14. Lebensjahr eine chronische Psoriasis ( Schuppenflechte ) und die ist in den letzten Wochen wie von Geisterhand an manchen Stellen verschwunden. Ich wünsche Euch allen alles Liebe, <user>}{September 2009、vor acht Wochen、Tamoxifen、Hitzewellen、ca. 9 kg in zwei Jahren zugenommen、Letroblock、Femara 、typische Hitzewellen、Schmerzen、Beine、chronische Psoriasis、Schuppenflechte、Euch allen、Liebe、ganz fürchterliche Schmerzen}\
                    输出：{药品名称：Tamoxifen、Letroblock、Femara，副作用：Hitzewellen、ca. 9 kg in zwei Jahren zugenommen、Hitzewellen、ganz fürchterliche Schmerzen、chronische Psoriasis、Schuppenflechte}",
                },
                {
                    "role": "assistant",
                    "content": "好的，我为您筛选出了实体列表中的药品名称和副作用实",
                },
                {
                    "role": "user",
                    "content": f"请根据{list}的语境，找出下列{str1}中药物名称以及副作用",
                },
            ],
        )
        str2 = response.choices[0].message
    except Exception as e:
        logger.error(f"Encounter error: {repr(e)} in second step")
        error_records["No"].append(i)
        error_records["Sample"].append(list)
        error_records["Error Message"].append(repr(e))
        error_records["Error Timing Step"].append(2)

    logger.info(f"[{i+1}] 待处理样本：{list}")
    logger.info(f"[{i+1}] 第一次处理结果：{str1}")
    logger.info(f"[{i+1}] 第二次处理结果：{str2}")

    ADE = pd.DataFrame(str2)
    outputresult = pd.DataFrame(outputresult)
    outputresult = pd.concat([outputresult, ADE])

logger.info(f"Totally {i+1} samples processed.")

outputresult.to_csv("./test_result_data/result.csv")
# 消除冗余数据
df = pd.read_csv("./test_result_data/result.csv")
df.columns = ["no", "content", "ADE"]
df = df[df.iloc[:, 0] != 1]
df = df[df.iloc[:, 0] != 2]
df = df.drop("no", axis="columns")
df = df.drop("content", axis="columns")
df.to_csv("./test_result_data/result.csv", index=False, encoding="utf-8")

pd.DataFrame(error_records).to_csv(
    "log/error_records.csv", index=False, encoding="utf-8"
)