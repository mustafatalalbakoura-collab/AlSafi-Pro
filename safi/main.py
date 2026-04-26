import flet as ft
import yfinance as yf
import pandas as pd

# دالة حساب المؤشرات الفنية يدوياً لضمان استقرار التطبيق
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def get_market_signal(pair):
    try:
        # جلب بيانات آخر يومين بفريم 5 دقائق
        df = yf.download(pair, period='2d', interval='5m', progress=False)
        if df.empty:
            return "لا توجد بيانات", "#808080", 0
        
        # حساب RSI
        df['RSI'] = calculate_rsi(df['Close'])
        last_rsi = df['RSI'].iloc[-1]
        last_price = df['Close'].iloc[-1]
        
        # منطق التحليل
        if last_rsi < 30:
            return "شراء قوي 🟢 (تشبع بيعي)", "#00FF00", last_price
        elif last_rsi > 70:
            return "بيع قوي 🔴 (تشبع شرائي)", "#FF4444", last_price
        else:
            return "سوق عرضي 🟡 (انتظر)", "#FFD700", last_price
    except Exception as e:
        return f"خطأ في الاتصال", "#FF4444", 0

def main(page: ft.Page):
    # إعدادات الصفحة
    page.title = "AlSafi Pro - رادار التداول"
    page.theme_mode = ft.ThemeMode.DARK
    page.rtl = True
    page.bgcolor = "#000000"  # أسود فخم
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # واجهة المستخدم
    title = ft.Text("رادار الصافي الذكي 📈", size=30, color="#FFD700", weight=ft.FontWeight.BOLD)
    
    pair_dropdown = ft.Dropdown(
        label="اختر الزوج أو السلعة",
        value="EURUSD=X",
        width=300,
        options=[
            ft.dropdown.Option("EURUSD=X", "يورو / دولار (EUR/USD)"),
            ft.dropdown.Option("GC=F", "الذهب (Gold)"),
            ft.dropdown.Option("BTC-USD", "البيتكوين (Bitcoin)"),
        ],
    )

    result_text = ft.Text("اضغط على تحديث لبدء التحليل", size=18, color="white")
    price_text = ft.Text("", size=22, color="#FFD700", weight=ft.FontWeight.W_500)
    
    status_container = ft.Container(
        content=result_text,
        padding=20,
        border_radius=15,
        bgcolor="#1a1a1a",
        alignment=ft.alignment.center,
        width=350
    )

    def on_update_click(e):
        status_container.content = ft.ProgressRing(width=20, height=20, color="#FFD700")
        page.update()
        
        signal, color, price = get_market_signal(pair_dropdown.value)
        
        status_container.bgcolor = color
        status_container.content = ft.Text(signal, size=20, color="black" if color != "#1a1a1a" else "white", weight="bold")
        price_text.value = f"السعر الحالي: {price:.5f}" if price > 0 else ""
        page.update()

    update_btn = ft.ElevatedButton(
        "تحديث التحليل الآن",
        icon=ft.icons.REFRESH,
        on_click=on_update_click,
        style=ft.ButtonStyle(
            color="black",
            bgcolor="#FFD700",
            padding=20
        )
    )

    # إضافة العناصر للصفحة
    page.add(
        ft.Column(
            [
                title,
                ft.Divider(color="#FFD700"),
                pair_dropdown,
                ft.VerticalDivider(height=20),
                status_container,
                price_text,
                ft.VerticalDivider(height=20),
                update_btn,
                ft.Text("صمم خصيصاً لعائلة باكورا - باشورة", size=12, color="#555555")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    # للعمل كموقع ويب وكـ APK في نفس الوقت
    ft.app(target=main)
  
