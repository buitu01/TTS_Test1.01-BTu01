import flet as ft
from flet_audio import Audio
from tts_engine import TTSEngine
import os

def main(page: ft.Page):
    page.title = "Text to Speech - Antigravity"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window_width = 600
    page.window_height = 800
    page.scroll = ft.ScrollMode.AUTO

    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    tts = TTSEngine(assets_dir)
    
    audio_player = Audio(src="", autoplay=True)
    page.overlay.append(audio_player)
    
    title = ft.Text("Text to Speech (AI Voices)", size=26, weight=ft.FontWeight.BOLD)
    
    textbox = ft.TextField(
        multiline=True, 
        min_lines=6, 
        max_lines=8, 
        value="Xin chào! Bạn có thể chọn giữa Edge-TTS, FPT.AI hoặc ElevenLabs ở bên dưới nhé.",
        border_color=ft.Colors.BLUE_400
    )

    # --- Tab Edge-TTS ---
    edge_voice_dropdown = ft.Dropdown(
        label="Giọng đọc",
        options=[
            ft.dropdown.Option("vi-VN-HoaiMyNeural", "Hoài My (Nữ)"),
            ft.dropdown.Option("vi-VN-NamMinhNeural", "Nam Minh (Nam)")
        ],
        value="vi-VN-HoaiMyNeural"
    )
    edge_speed_slider = ft.Slider(min=-50, max=50, divisions=100, label="Tốc độ: {value}%", value=0)
    edge_expr_dropdown = ft.Dropdown(
        label="Biểu cảm",
        options=[ft.dropdown.Option(x) for x in ["Bình thường", "Vui vẻ", "Buồn bã", "Ngạc nhiên", "Tức giận"]],
        value="Bình thường"
    )

    # --- Tab FPT.AI ---
    fpt_voice_dropdown = ft.Dropdown(
        label="Giọng đọc",
        options=[
            ft.dropdown.Option("banmai", "banmai (Nữ miền Bắc)"),
            ft.dropdown.Option("thuminh", "thuminh (Nữ miền Bắc)"),
            ft.dropdown.Option("leminh", "leminh (Nam miền Bắc)"),
            ft.dropdown.Option("ngoclam", "ngoclam (Nữ miền Trung)"),
            ft.dropdown.Option("giahuy", "giahuy (Nam miền Trung)"),
            ft.dropdown.Option("minhquang", "minhquang (Nam miền Nam)"),
            ft.dropdown.Option("linhsan", "linhsan (Nữ miền Nam)")
        ],
        value="banmai"
    )
    fpt_speed_slider = ft.Slider(min=-3, max=3, divisions=6, label="Tốc độ: {value}", value=0)

    # --- Tab ElevenLabs ---
    eleven_voices_map = {
        "Na15FlRRkMEDtEW4nVVP": "Thanh Ngọc",
        "FTYCiQT21H9XQvhRu0ch": "Trung",
        "HQZkBNMmZF5aISnrU842": "MC Khánh Ly",
        "a3AkyqGG4v8Pg7SWQ0Y3": "Ngân Baby",
        "3VnrjnYrskPMDsapTr8X": "Hùng"
    }
    eleven_voice_dropdown = ft.Dropdown(
        label="Giọng đọc (Tiếng Việt)",
        options=[ft.dropdown.Option(k, v) for k, v in eleven_voices_map.items()],
        value="Na15FlRRkMEDtEW4nVVP"
    )
    eleven_custom_input = ft.TextField(label="Hoặc nhập Voice ID", hint_text="Nếu bạn tự clone giọng")

    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(label="Edge-TTS"),
            ft.Tab(label="FPT.AI"),
            ft.Tab(label="ElevenLabs")
        ]
    )

    tab_view = ft.TabBarView(
        controls=[
            ft.Container(
                padding=20,
                content=ft.Column([
                    edge_voice_dropdown,
                    ft.Text("Điều chỉnh Tốc độ:"),
                    edge_speed_slider,
                    edge_expr_dropdown
                ])
            ),
            ft.Container(
                padding=20,
                content=ft.Column([
                    fpt_voice_dropdown,
                    ft.Text("Điều chỉnh Tốc độ:"),
                    fpt_speed_slider
                ])
            ),
            ft.Container(
                padding=20,
                content=ft.Column([
                    eleven_voice_dropdown,
                    eleven_custom_input,
                    ft.Text("Lưu ý: Công nghệ Đa ngôn ngữ tự động nhận diện và phát âm chuẩn tiếng Việt.", color=ft.Colors.GREY, size=12)
                ])
            )
        ],
        expand=True
    )

    tabs = ft.Tabs(
        length=3,
        selected_index=0,
        content=ft.Column([tab_bar, tab_view], expand=True),
        expand=True
    )

    status_text = ft.Text("Sẵn sàng", color=ft.Colors.GREY)
    
    def on_audio_state_changed(e):
        if e.data == "completed":
            play_btn.disabled = False
            status_text.value = "Đã phát xong."
            page.update()

    audio_player.on_state_changed = on_audio_state_changed

    def play_click(e):
        text = textbox.value.strip()
        if not text:
            status_text.value = "Vui lòng nhập văn bản!"
            page.update()
            return
            
        play_btn.disabled = True
        status_text.value = "Đang tổng hợp giọng nói..."
        page.update()

        tab_idx = tabs.selected_index
        kwargs = {}
        if tab_idx == 0:
            kwargs = {
                "engine": "edge",
                "voice": edge_voice_dropdown.value,
                "expression": edge_expr_dropdown.value,
                "speed_modifier": f"{int(edge_speed_slider.value):+}%"
            }
        elif tab_idx == 1:
            kwargs = {
                "engine": "fpt",
                "voice": fpt_voice_dropdown.value,
                "fpt_speed": str(int(fpt_speed_slider.value)),
                "fpt_api_key": "8kHsOAfRLEWN22TTvx4Pne2Dsilyq2NZ"
            }
        elif tab_idx == 2:
            vid = eleven_custom_input.value.strip()
            if not vid:
                vid = eleven_voice_dropdown.value
            kwargs = {
                "engine": "elevenlabs",
                "voice": vid,
                "eleven_api_key": "sk_dc47762bcfed41e25d9d5aeda2e2a6194be3016d850d95e1"
            }
        
        try:
            filename = tts.generate_sync(text, **kwargs)
            audio_player.src = filename
            audio_player.update()
            status_text.value = "Đang phát..."
        except Exception as ex:
            status_text.value = f"Lỗi: {ex}"
            play_btn.disabled = False
            
        page.update()

    play_btn = ft.ElevatedButton(
        "▶ Đọc văn bản", 
        on_click=play_click, 
        bgcolor=ft.Colors.GREEN_700, 
        color=ft.Colors.WHITE,
        height=50,
        width=200
    )
    
    page.add(
        ft.Row([title], alignment=ft.MainAxisAlignment.CENTER),
        textbox,
        tabs,
        ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([play_btn], alignment=ft.MainAxisAlignment.CENTER)
    )

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
