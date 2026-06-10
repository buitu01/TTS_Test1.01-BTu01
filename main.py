import flet as ft
import flet_audio
from tts_engine import TTSEngine
import os

def main(page: ft.Page):
    page.title = "Text to Speech - Antigravity"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A" # Premium Slate 900
    page.window_width = 400
    page.window_height = 800
    page.padding = 0 # Remove default padding so bottom bar touches edges
    
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    tts = TTSEngine(assets_dir)
    
    audio_player = flet_audio.Audio(src="", autoplay=True)
    
    # Custom colors
    ACCENT_COLOR = "#3B82F6" # Blue 500
    TEXT_COLOR = "#F8FAFC" # Slate 50
    CARD_BG = "#1E293B" # Slate 800
    
    title = ft.Text("AI Voice Studio", size=28, weight=ft.FontWeight.W_800, color=TEXT_COLOR)
    
    textbox = ft.TextField(
        multiline=True, 
        min_lines=5, 
        max_lines=7, 
        value="Xin chào! Bạn có thể chọn giữa Edge-TTS, FPT.AI hoặc ElevenLabs ở bên dưới nhé.",
        border_color="transparent",
        bgcolor=CARD_BG,
        color=TEXT_COLOR,
        border_radius=15,
        content_padding=20,
        text_size=16,
        cursor_color=ACCENT_COLOR,
        focused_border_color=ACCENT_COLOR,
        focused_border_width=2
    )

    # --- Tab Edge-TTS ---
    edge_voice_dropdown = ft.Dropdown(
        label="Giọng đọc",
        options=[
            ft.dropdown.Option("vi-VN-HoaiMyNeural", "Hoài My (Nữ)"),
            ft.dropdown.Option("vi-VN-NamMinhNeural", "Nam Minh (Nam)")
        ],
        value="vi-VN-HoaiMyNeural",
        border_radius=10,
        filled=True,
        bgcolor=page.bgcolor
    )
    edge_speed_slider = ft.Slider(min=-50, max=50, divisions=100, label="Tốc độ: {value}%", value=0, active_color=ACCENT_COLOR)
    edge_expr_dropdown = ft.Dropdown(
        label="Biểu cảm",
        options=[ft.dropdown.Option(x) for x in ["Bình thường", "Vui vẻ", "Buồn bã", "Ngạc nhiên", "Tức giận"]],
        value="Bình thường",
        border_radius=10,
        filled=True,
        bgcolor=page.bgcolor
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
        value="banmai",
        border_radius=10,
        filled=True,
        bgcolor=page.bgcolor
    )
    fpt_speed_slider = ft.Slider(min=-3, max=3, divisions=6, label="Tốc độ: {value}", value=0, active_color=ACCENT_COLOR)

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
        value="Na15FlRRkMEDtEW4nVVP",
        border_radius=10,
        filled=True,
        bgcolor=page.bgcolor
    )
    eleven_custom_input = ft.TextField(
        label="Hoặc nhập Voice ID", 
        hint_text="Nếu bạn tự clone giọng",
        border_radius=10,
        filled=True,
        bgcolor=page.bgcolor
    )

    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(text="Edge-TTS"),
            ft.Tab(text="FPT.AI"),
            ft.Tab(text="ElevenLabs")
        ],
        indicator_color=ACCENT_COLOR,
        label_color=ACCENT_COLOR,
        unselected_label_color=ft.Colors.GREY_500
    )

    tab_view = ft.TabBarView(
        controls=[
            ft.Container(
                padding=20,
                content=ft.Column([
                    edge_voice_dropdown,
                    ft.Text("Tốc độ", size=14, color=ft.Colors.GREY_400, weight=ft.FontWeight.W_600),
                    edge_speed_slider,
                    edge_expr_dropdown
                ], scroll=ft.ScrollMode.AUTO)
            ),
            ft.Container(
                padding=20,
                content=ft.Column([
                    fpt_voice_dropdown,
                    ft.Text("Tốc độ", size=14, color=ft.Colors.GREY_400, weight=ft.FontWeight.W_600),
                    fpt_speed_slider
                ], scroll=ft.ScrollMode.AUTO)
            ),
            ft.Container(
                padding=20,
                content=ft.Column([
                    eleven_voice_dropdown,
                    eleven_custom_input,
                    ft.Text("Công nghệ AI Đa ngôn ngữ tự động phát âm chuẩn xác Tiếng Việt.", color=ft.Colors.GREY_500, size=13, italic=True)
                ], scroll=ft.ScrollMode.AUTO)
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

    status_text = ft.Text("Sẵn sàng", color=ft.Colors.GREY_400, size=14, weight=ft.FontWeight.W_500)
    
    def on_audio_state_changed(e):
        if e.data == "completed":
            play_btn.disabled = False
            play_btn.content.controls[0].name = ft.Icons.PLAY_ARROW_ROUNDED
            play_btn.content.controls[1].value = "Phát lại"
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
        play_btn.content.controls[0].name = ft.Icons.HOURGLASS_EMPTY
        play_btn.content.controls[1].value = "Đang xử lý..."
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
            play_btn.content.controls[0].name = ft.Icons.VOLUME_UP_ROUNDED
            play_btn.content.controls[1].value = "Đang phát..."
        except Exception as ex:
            status_text.value = f"Lỗi: {ex}"
            play_btn.disabled = False
            play_btn.content.controls[0].name = ft.Icons.PLAY_ARROW_ROUNDED
            play_btn.content.controls[1].value = "Thử lại"
            
        page.update()

    play_btn = ft.Container(
        content=ft.Row([
            ft.Icon(name=ft.Icons.PLAY_ARROW_ROUNDED, color=ft.Colors.WHITE, size=24),
            ft.Text("Đọc văn bản", size=18, weight=ft.FontWeight.W_700, color=ft.Colors.WHITE)
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=ACCENT_COLOR,
        padding=15,
        border_radius=30,
        on_click=play_click,
        ink=True, # Ripple effect
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=15, color=ft.colors.with_opacity(0.4, ACCENT_COLOR), offset=ft.Offset(0, 4))
    )
    
    # Main content wrapper
    content = ft.Column(
        controls=[
            ft.Container(
                content=title,
                padding=ft.padding.only(top=15, bottom=15, left=20, right=20)
            ),
            ft.Container(
                content=textbox,
                padding=ft.padding.only(left=20, right=20, bottom=10)
            ),
            ft.Container(
                content=tabs,
                expand=True,
                bgcolor=CARD_BG,
                border_radius=ft.border_radius.only(top_left=30, top_right=30),
                padding=ft.padding.only(top=10)
            )
        ],
        expand=True,
        spacing=0
    )

    # Bottom action bar (fixed at bottom)
    bottom_bar = ft.Container(
        content=ft.Column([
            ft.Row([status_text], alignment=ft.MainAxisAlignment.CENTER),
            play_btn,
            ft.Container(audio_player, width=0, height=0)
        ], spacing=15),
        padding=ft.padding.only(left=20, right=20, top=15, bottom=ft.padding.WindowPadding.bottom + 25),
        bgcolor=CARD_BG,
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=20, color=ft.Colors.BLACK)
    )

    # The layout structure
    layout = ft.Column(
        controls=[
            ft.Container(content=content, expand=True),
            bottom_bar
        ],
        expand=True,
        spacing=0
    )

    page.add(ft.SafeArea(layout, expand=True))

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
