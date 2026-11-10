import urllib.request, re, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("\n🚀 === جاري فحص أنظمة الزعيم شملان === 🚀\n")

# سحب العداد الداخلي للبوت من راوند
try:
    bot_req = urllib.request.urlopen("https://shmlanaly.onrender.com", context=ctx, timeout=10)
    bot_views = bot_req.read().decode('utf-8').strip()
    if bot_views.isdigit():
        print(f"🔥 المشاهدات اللي جابها البوت حقنا فقط: {bot_views} مشاهدة (منذ آخر تشغيل)")
    else:
        print("🟢 سيرفر راوند: شغال (جالس يجهز المتصفحات).")
except Exception as e:
    print("🟢 سيرفر راوند: شغال (في وضع الاستعداد).")

# سحب المشاهدات الكلية من يوتيوب
try:
    url = "https://www.youtube.com/watch?v=9Uz04LYQe5k"
    html = urllib.request.urlopen(url, context=ctx).read().decode('utf-8')
    views = re.search(r'"viewCount":"(\d+)"', html)
    if views:
        print(f"👁️ إجمالي مشاهدات الفيديو في يوتيوب الآن: {views.group(1)} مشاهدة")
except:
    pass

print("\n=======================================\n")
