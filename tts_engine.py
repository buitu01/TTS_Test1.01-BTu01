import asyncio
import edge_tts
import os
import uuid
import glob
import requests
import time
import json

EXPRESSIONS = {
    "Bình thường": {"rate": "+0%", "pitch": "+0Hz"},
    "Vui vẻ": {"rate": "+15%", "pitch": "+10Hz"},
    "Buồn bã": {"rate": "-15%", "pitch": "-15Hz"},
    "Ngạc nhiên": {"rate": "+5%", "pitch": "+20Hz"},
    "Tức giận": {"rate": "+15%", "pitch": "-10Hz"},
}

class TTSEngine:
    def __init__(self, assets_dir):
        self.assets_dir = assets_dir
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)

    def cleanup_temp_files(self):
        for f in glob.glob(os.path.join(self.assets_dir, "temp_audio_*.mp3")):
            try: os.remove(f)
            except: pass

    async def _async_generate_edge(self, text, voice, rate, pitch, output_file):
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await communicate.save(output_file)

    def generate_sync(self, text, engine="edge", voice="vi-VN-HoaiMyNeural", expression="Bình thường", speed_modifier="+0%", fpt_api_key="", fpt_speed="0", eleven_api_key=""):
        self.cleanup_temp_files()
        filename = f"temp_audio_{uuid.uuid4().hex[:8]}.mp3"
        output_file = os.path.join(self.assets_dir, filename)

        if engine == "edge":
            base_rate = int(EXPRESSIONS.get(expression, EXPRESSIONS["Bình thường"])["rate"].replace("%", "").replace("+", ""))
            speed_mod = int(speed_modifier.replace("%", "").replace("+", ""))
            final_rate = f"{base_rate + speed_mod:+}%"
            pitch = EXPRESSIONS.get(expression, EXPRESSIONS["Bình thường"])["pitch"]
            
            asyncio.run(self._async_generate_edge(text, voice, final_rate, pitch, output_file))
            
        elif engine == "fpt":
            url = 'https://api.fpt.ai/hmi/tts/v5'
            headers = {
                'api-key': fpt_api_key,
                'speed': str(fpt_speed),
                'voice': voice
            }
            response = requests.post(url, data=text.encode('utf-8'), headers=headers)
            res_json = response.json()
            
            if str(res_json.get('error')) == '0':
                audio_url = res_json.get('async')
                success = False
                for _ in range(30):
                    audio_res = requests.get(audio_url)
                    if audio_res.status_code == 200 and audio_res.headers.get('Content-Type', '').startswith('audio'):
                        with open(output_file, 'wb') as f:
                            f.write(audio_res.content)
                        success = True
                        break
                    time.sleep(1)
                if not success:
                    raise Exception("Timeout khi đợi phản hồi file mp3 từ FPT.AI.")
            else:
                raise Exception(res_json.get('message', 'Lỗi từ FPT API'))
                
        elif engine == "elevenlabs":
            url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice}'
            headers = {
                'xi-api-key': eleven_api_key,
                'Content-Type': 'application/json'
            }
            payload = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                with open(output_file, 'wb') as f:
                    f.write(response.content)
            else:
                err_msg = response.text
                try:
                    err_msg = response.json().get("detail", {}).get("message", response.text)
                except:
                    pass
                raise Exception(f"Lỗi ElevenLabs: {err_msg}")

        return filename

    def save_to_file(self, text, output_path, engine="edge", voice="vi-VN-HoaiMyNeural", expression="Bình thường", speed_modifier="+0%", fpt_api_key="", fpt_speed="0", eleven_api_key=""):
        temp_filename = self.generate_sync(text, engine, voice, expression, speed_modifier, fpt_api_key, fpt_speed, eleven_api_key)
        import shutil
        shutil.copy(os.path.join(self.assets_dir, temp_filename), output_path)
