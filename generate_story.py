import base64
import json
import os
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
sample_path = ROOT / "voice_sample_direct.wav"
output_path = ROOT / "我的音色-讲故事-中气更足-男性版.wav"

voice_base64 = base64.b64encode(sample_path.read_bytes()).decode("utf-8")

story = """(男性 低沉 深沉 沉浸 中气饱满)
在离海边不远的小镇上，有一座谁也说不清建了多久的钟楼。它没有钟面，也没有指针，只有每到月圆之夜，才会从塔顶传来一声悠长的钟响。

镇上的老人说，那是钟楼在提醒迷路的人：只要抬头看见月亮，就一定能找到回家的路。可是有一年冬天，一个叫阿澜的女孩，在暴风雪里走丢了。她抱着一盏快要熄灭的小灯，沿着陌生的山路走啊，走啊，直到雪花盖住了她的脚印。

就在她以为自己再也回不去的时候，远处忽然传来钟声。第一声，像是从云层深处落下来；第二声，像有人在黑暗里轻轻敲门。阿澜抬起头，看见月光穿过风雪，在山坡上铺出一条银色的小路。

她沿着那条路走了很久，终于在天亮前回到了小镇。多年以后，阿澜成了钟楼的守望人。每逢月圆，她都会点亮塔顶的灯，然后对着远方轻声说：别害怕，抬头看看，回家的路一直都在。"""

payload = {
    "model": "mimo-v2.5-tts-voiceclone",
    "messages": [
        {
            "role": "user",
            "content": (
                "请用温暖、沉浸、富有画面感的中文故事讲述方式来演绎。"
                "请用成年男性的沉稳、低沉声线来讲述，声音更饱满、更有支撑，"
                "气息充足，胸腔共鸣明显，中气更足、音量稳定而有感染力，"
                "但不要喊叫或过度夸张；吐字清晰，"
                "句间停顿自然；开头平静，"
                "暴风雪部分略微紧张，结尾回归温柔和安定，像在夜晚给人讲一个寓言故事。"
            ),
        },
        {"role": "assistant", "content": story},
    ],
    "audio": {
        "format": "wav",
        "voice": f"data:audio/wav;base64,{voice_base64}",
    },
}

request = urllib.request.Request(
    "https://api.xiaomimimo.com/v1/chat/completions",
    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
    headers={
        "Authorization": f"Bearer {os.environ['MIMO_API_KEY']}",
        "Content-Type": "application/json",
    },
    method="POST",
)

with urllib.request.urlopen(request, timeout=300) as response:
    result = json.loads(response.read().decode("utf-8"))

audio_data = result["choices"][0]["message"]["audio"]["data"]
if not audio_data:
    raise RuntimeError("MiMo API 未返回音频数据")

output_path.write_bytes(base64.b64decode(audio_data))
print(output_path)
