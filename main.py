import os
import re
import pytz
import requests
import threading
import telebot
from datetime import datetime, time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8839060416:AAF2Ie6pE4_gfWPk-WdVDfDzHaTO3yf6jHc"
ADMIN_ID = 6454550864  
AUDIO_URL = "https://www.islam4u.com/sites/default/files/adiieh/%D8%AF%D8%B9%D8%A7%D8%A1%20%D8%A7%D9%84%D8%B9%D9%87%D8%AF%20%D8%A8%D8%B5%D9%88%D8%AA%20%D8%A7%D9%84%D9%82%D8%A7%D8%B1%D8%A6%20%D8%A7%D9%84%D8%B3%D9%8A%D8%AF%D8%B9%D8%A8%D8%AF%D8%A7%D9%84%D8%AD%D9%84%D9%8A%D9%85%20%D8%A7%D9%84%D9%86%D9%88%D8%B1%D8%A7%D9%86%D9%8A.mp3"
FIREBASE_URL = "https://al-ahad-a43d8-default-rtdb.firebaseio.com/users"

bot = telebot.TeleBot(BOT_TOKEN)
TZ_BAGHDAD = pytz.timezone("Asia/Baghdad")

def load_data():
    try:
        response = requests.get(f"{FIREBASE_URL}.json", timeout=10)
        if response.status_code == 200 and response.json():
            return response.json()
    except Exception as e:
        print(f"خطأ في جلب البيانات: {e}")
    return {}

def save_data(data):
    try:
        requests.put(f"{FIREBASE_URL}.json", json=data, timeout=10)
    except Exception as e:
        print(f"خطأ في حفظ البيانات: {e}")

def update_user_field(user_id, user_data):
    try:
        requests.patch(f"{FIREBASE_URL}/{user_id}.json", json=user_data, timeout=10)
    except Exception as e:
        print(f"خطأ في تحديث بيانات المستخدم: {e}")

def get_dates():
    url = "https://www.sistani.org"
    headers = {
        'User-Agent': "Mozilla/5.0 (Linux; Android 11; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        'referer': "https://www.google.com/",
        'accept-language': "ar-DZ,ar;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        res = re.search(r'style="margin-left:9px;">([^<]+)</span>', response.text)
        if res:
            hijri_date = res.group(1).strip()
            now = datetime.now(TZ_BAGHDAD)
            gregorian_date = now.strftime("%Y-%m-%d")
            return f"ميلادي: {gregorian_date} \n هجري: {hijri_date}"
    except Exception as e:
        print(f"خطأ في جلب التاريخ: {e}")
    
    now = datetime.now(TZ_BAGHDAD)
    return now.strftime("التاريخ: %Y-%m-%d")

DUAA_TEXT = """
<blockquote> \t \t \t بِسْمِ اللهِ الرَّحْمَنِ الرَّحِيمِ</blockquote>

اَللَّهُمَّ رَبَّ النُّورِ الْعَظِيمِ وَرَبَّ الْكُرْسِيِّ الرَّفِيعِ وَرَبَّ الْبَحْرِ الْمَسْجُورِ وَمُنْزِلَ التَّوْرَاةِ وَالإِنْجِيلِ وَالزَّبُورِ وَرَبَّ الظِّلِّ وَالْحَرُورِ وَمُنْزِلَ الْقُرْآنِ العَظِيمِ وَرَبَّ الْمَلائِكَةِ الْمُقَرَّبِينَ وَالأَنْبِيَاءِ وَالْمُرْسَلِينَ.

اَللَّهُمَّ إِنِّي أَسْأَلُكَ بِوَجْهِكَ الْكَرِيمِ وَبِنُورِ وَجْهِكَ الْمُنِيرِ وَمُلْكِكَ القَدِيمِ، يَا حَيُّ يَا قَيُّومُ أَسْأَلُكَ بِاسْمِكَ الَّذِي أَشْرَقَتْ بِهِ السَّمَاوَاتُ وَالأَرَضُونَ وَبِاسْمِكَ الَّذِي يَصْلُحُ بِهِ الأوَّلُونَ وَالآخِرُونَ، يَا حَيًّا قَبْلَ كُلِّ حَيٍّ وَيَا حَيًّا بَعْدَ كُلِّ حَيٍّ وَيَا حَيًّا حِينَ لا حَيَّ يَا مُحْيِيَ الْمَوْتَى وَمُمِيتَ الأَحْياءِ يَا حَيُّ لا إِلَهَ إِلَّا أَنْتَ.

اَللَّهُمَّ بَلِّغْ مَوْلانَا الإِمَامَ الْهَادِيَ الْمَهْدِيَّ الْقَائِمَ بِأَمْرِكَ ـ صَلوَاتُ اللهِ عَلَيْهِ وَعَلَى آبَائِهِ الطَّاهِرِينَ ـ عَنْ جَمِيعِ الْمُؤْمِنِينَ وَالْمُؤْمِنَاتِ فِي مَشَارِقِ الأَرْضِ وَمَغَارِبهَا سَهْلِهَا وَجَبَلِهَا وَبَرِّهَا وَبَحْرِهَا وَعَنِّي وَعَن وَّالِدَيَّ مِنَ الصَّلَوَاتِ زِنَةَ عَرْشِ اللهِ وَمِدَادَ كَلِمَاتِهِ وَمَا أحْصَاهُ عِلْمُهُ وَأَحَاطَ بِهِ كِتَابُهُ.

اَللَّهُمَّ إِنِّي أُجَدِّدُ لَهُ فِي صَبِيحةِ يَوْمِي هَذَا وَمَا عِشْتُ مِنْ أَيَّامِي عَهْداً وَعَقْداً وَبَيْعَةً لَهُ فِي عُنُقِي لا أَحُولُ عَنْهَا وَلا أَزُولُ أَبَداً.

اَللَّهُمَّ اجْعَلْنِي مِنْ أَنْصَارِهِ وَأَعْوَانِهِ وَالذَّابِّينَ عَنْهُ وَالْمُسَارِعِينَ إِلَيْهِ فِي قَضاءِ حَوَائِجِهِ وَالْمُمْتَثِلِينَ لِأَوَامِرِهِ وَالْمُحَامِينَ عَنْهُ وَالسَّابِقِينَ إِلَى إِرَادَتِهِ وَالْمُسْتَشْهَدِينَ بَيْنَ يَدَيْهِ.

اَللَّهُمَّ إِنْ حَالَ بَيْنِي وَبَيْنَهُ الْمَوْتُ الَّذِي جَعَلْتَهُ عَلَى عِبَادِكَ حَتْماً مَقْضِيًّا فَأَخْرِجْنِي مِنْ قَبْرِي مُؤْتَزِراً كَفَنِي شَاهِراً سَيْفِي مُجَرِّداً قَنَاتِي مُلَبِّياً دَعْوَةَ الدَّاعِي فِي الْحَاضِرِ وَالْبَادِي.

اَللَّهُمَّ أَرِنِي الطَّلْعَةَ الرَّشِيدَةَ وَالْغُرَّةَ الْحَمِيدَةَ وَاكْحُلْ ناظِرِي بِنَظْرَةٍ مِّنِّي إِلَيْهِ وَعَجِّلْ فَرَجَهُ وَسَهِّلْ مَخْرَجَهُ وَأَوْسِعْ مَنْهَجَهُ وَاسْلُكْ بِي مَحَجَّتَهُ وَأَنْفِذْ أَمْرَهُ وَاشْدُدْ أَزْرَهُ.

وَاعْمُرِ ـ اللَّهُمَّ ـ بِهِ بِلادَكَ وَأَحْيِ بِه عِبَادَكَ فَإِنَّكَ قُلْتَ وَقَوْلُكَ الْحَقُّ: <b>﴿ظَهَرَ الْفَسَادُ فِي الْبَرِّ وَالْبَحْرِ بِمَا كَسَبَتْ أَيْدِي النَّاسِ﴾</b>.

فَأَظْهِرِ ـ اللَّهُمَّ ـ لَنا وَلِيَّكَ وَابْنَ بِنْتِ نَبِيِّكَ الْمُسَمّى بِاسْمِ رَسُولِكَ حَتَّى لا يَظْفَرَ بِشَيْءٍ مِنَ الْبَاطِلِ إِلَّا مَزَّقَهُ وَيَحِقَّ الْحَقَّ وَيُحَقِّقَهُ، وَاجْعَلْهُ ـ اللّهُمَّ ـ مَفْزَعاً لِمَظْلُومِ عِبَادِكَ وَنَاصِراً لِمْن لَّا يَجِدُ لَهُ ناصِراً غَيْرَكَ وَمُجَدِّداً لِمَا عُطِّلَ مِنْ أَحْكَامِ كِتَابِكَ وَمُشَيِّداً لِّمَا وَرَدَ مِنْ أَعْلامِ دِينِكَ وَسُنَنِ نَبِيِّكَ ـ صَلَّى اللهُ عَلَيْهِ وَآلِهِ ـ، وَاجْعَلْهُ ـ اللَّهُمَّ ـ مِمَّنْ حَصَّنْتَهُ مِنْ بَأْسِ الْمُعْتَدِينَ.

اَللَّهُمَّ وَسُرَّ نَبِيَّكَ مُحَمَّداً ـ صَلَّى اللهُ عَلَيْهِ وَآلِهِ ـ بِرُؤْيَتِهِ وَمَنْ تَبِعَهُ عَلَى دَعْوَتِهِ وَارْحَمِ اسْتِكانَتَنَا بَعْدَهُ، اَللَّهُمَّ اكْشِفْ هَذِهِ الْغُمَّةَ عَنْ هَذِهِ الأُمَّةِ بِحُضُورِهِ وَعَجِّل لَّنَا ظُهُورَهُ <b>﴿إِنَّهُمْ يَرَوْنَهُ بَعِيداً وَنَرَاهُ قَرِيباً﴾</b> بِرَحْمَتِكَ يَا أَرْحَمَ الرَّاحِمِينَ.

<blockquote><b>ثمّ تضرب على فخذك الأيمن بيدك ثلاث مرّات وتقول كلّ مرّة:</b>
الْعَجَلَ الْعَجَلَ يَا مَوْلايَ يَا صَاحِبَ الزَّمَانِ.</blockquote>
"""

@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or ""
    data = load_data()
    
    if user_id not in data:
        data[user_id] = {
            "active": True,
            "streak": 0,
            "cycles": 0,
            "last_read_date": "",
            "today_sent": False,
            "last_msg_id": None,
            "username": username
        }
        update_user_field(user_id, data[user_id])

    user = data[user_id]
    is_active = user["active"]
    btn_text = "🔕 إيقاف التفعيل" if is_active else "🔔 تفعيل التذكير اليومي"
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(btn_text, callback_data="toggle_active"))
    
    status_str = "مفعّل بشكل تلقائي✅" if is_active else "متوقف ❌"
    date_info = get_dates()
    
    msg = (
        f"أهلاً بك عزيزي في بوت <b>دعاء العهد</b> 🤲\n\n"
        f"📅 <b>{date_info}</b>\n"
        f"حالة التذكير لديك: <b>{status_str}</b>\n\n"
        f"<blockquote>📊 <b>إحصائياتك الحالية (من قاعدة البيانات):</b>\n"
        f"• عدد أيام القراءة المتتالية: <b>{user['streak']}/40</b>\n"
        f"• دورات القراءة المكتملة: <b>{user['cycles']}</b>\n"
        f"• آخر تاريخ تسجيل: <b>{user.get('last_read_date') if user.get('last_read_date') else 'لم يسجل بعد'}</b></blockquote>\n\n"
        f"ℹ️ يُرسل الدعاء يومياً الساعة <b>5:00 صباحاً</b>، ومهلة التسجيل تنتهي الساعة <b>11:00 صباحاً</b>.\n"
        f"في حال فاتك الوقت ولم تسجل يتم تصفير عدد قراءاتك . "
    )
    bot.send_message(message.chat.id, msg, reply_markup=markup, parse_mode="HTML")
# معالجة أزرار التحكم بالعدادات
# معالجة أزرار التحكم بالعدادات
@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
def admin_callbacks(call):
    if call.from_user.id != ADMIN_ID:
        return
    
    # قائمة خيارات التحكم بالعدادات
    if call.data == "admin_control" or call.data == "admin_cancel":
        # مسح أية حالة تعيين سابقة عند الرجوع أو الإلغاء
        admin_states.pop(call.from_user.id, None)
        
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("➕ إضافة أيام", callback_data="admin_action_add_streak"),
            InlineKeyboardButton("➖ خصم أيام", callback_data="admin_action_sub_streak")
        )
        markup.add(
            InlineKeyboardButton("➕ إضافة دورات", callback_data="admin_action_add_cycles"),
            InlineKeyboardButton("➖ خصم دورات", callback_data="admin_action_sub_cycles")
        )
        markup.add(
            InlineKeyboardButton("🔄 تصفير الأيام", callback_data="admin_action_reset_streak"),
            InlineKeyboardButton("🗑 تصفير الدورات", callback_data="admin_action_reset_cycles")
        )
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🛠 <b>اختر الإجراء المطلوب للتحكم بالعدادات:</b>",
            reply_markup=markup,
            parse_mode="HTML"
        )
        
    # اختيار إجراء معين (إضافة / خصم)
    elif call.data.startswith("admin_action_"):
        action = call.data.replace("admin_action_", "")
        admin_states[call.from_user.id] = {"action": action}
        
        labels = {
            "add_streak": "إضافة أيام قراءة",
            "sub_streak": "خصم أيام قراءة",
            "add_cycles": "إضافة دورات",
            "sub_cycles": "خصم دورات",
            "reset_cycles": "تصفير دورات مستخدم"
        }
        
        # زر الرجوع / الإلغاء
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🔙 رجوع / إلغاء", callback_data="admin_cancel"))
        
        text = (
            f"📝 <b>أنت الآن تقوم بـ ({labels.get(action)}):</b>\n\n"
            f"يرجى إرسال الآيدي والعدد بفاصلة مسافة بالشكل التالي:\n"
            f"<code>الآيدي العدد</code>\n\n"
            f"مثال:\n<code>6454550864 5</code>"
        )
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=markup,
            parse_mode="HTML"
        )
# استقبال مدخلات التعديل من الأدمن
@bot.message_handler(func=lambda message: message.from_user.id == ADMIN_ID and message.from_user.id in admin_states)
def process_admin_input(message):
    action_info = admin_states.pop(message.from_user.id, None)
    if not action_info:
        return
    
    try:
        parts = message.text.strip().split()
        target_id = parts[0]
        value = int(parts[1])
        
        data = load_data()
        if target_id not in data or not isinstance(data[target_id], dict):
            bot.reply_to(message, "❌ هذا المستخدم غير موجود في قاعدة البيانات!")
            return
        
        user = data[target_id]
        action = action_info["action"]
        
        if action == "add_streak":
            user["streak"] = user.get("streak", 0) + value
        elif action == "sub_streak":
            user["streak"] = max(0, user.get("streak", 0) - value)
        elif action == "add_cycles":
            user["cycles"] = user.get("cycles", 0) + value
        elif action == "sub_cycles":
            user["cycles"] = max(0, user.get("cycles", 0) - value)
        elif action == "reset_streak":
            user["streak"] = 0
        elif action == "reset_cycles":
            user["cycles"] = 0    
        update_user_field(target_id, user)
        uname = f"@{user.get('username')}" if user.get('username') else "بدون يوزر"
        bot.reply_to(
            message,
            f"✅ <b>تم التعديل بنجاح!</b>\n\n"
            f"<blockquote>"
            f"• <b>اليوزر:</b> {uname}\n"
            f"  └ <b>الآيدي:</b> <code>{target_id}</code>\n"
            f"  └ <b>القراءات الحالية:</b> <code>{user.get('streak', 0)}/40</code> يوم\n"
            f"  └ <b>الدورات الحالية:</b> <code>{user.get('cycles', 0)}</code> دورة"
            f"</blockquote>",
            parse_mode="HTML"
        )
        
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ أثناء التعديل، التأكد من إدخال البيانات بصورة صحيحة (آيدي ثم مسافة ثم العدد).\nالخطأ: {e}")
# متغيرا للتفاعل مع إدخال الأدمن للتحكم
admin_states = {}

@bot.message_handler(commands=['admin'])
def admin_stats(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    data = load_data()
    total_users = len(data)
    active_users = sum(1 for u in data.values() if u.get("active") if isinstance(u, dict))
    
    total_streaks = sum(u.get("streak", 0) for u in data.values() if isinstance(u, dict))
    total_cycles = sum(u.get("cycles", 0) for u in data.values() if isinstance(u, dict))
    
    top_streak_user = None
    top_streak_val = -1
    top_cycle_user = None
    top_cycle_val = -1
    
    for uid, uinfo in data.items():
        if not isinstance(uinfo, dict):
            continue
        streak = uinfo.get("streak", 0)
        cycles = uinfo.get("cycles", 0)
        
        if streak > top_streak_val:
            top_streak_val = streak
            top_streak_user = (uid, uinfo.get("username", "بدون يوزر"))
            
        if cycles > top_cycle_val:
            top_cycle_val = cycles
            top_cycle_user = (uid, uinfo.get("username", "بدون يوزر"))

    report = "📊 <b>إحصائيات بوت دعاء العهد الشاملة</b>\n\n"
    report += (
        "<blockquote>"
        f"👥 إجمالي المستخدمين: <b>{total_users}</b>\n"
        f"🔔 المشتركين الفاعلين: <b>{active_users}</b>\n"
        f"📖 إجمالي القراءات المسجلة: <b>{total_streaks}</b>\n"
        f"🔄 إجمالي الدورات المكتملة: <b>{total_cycles}</b>"
        "</blockquote>\n\n"
    )
    
    if top_streak_user and top_streak_val >= 0:
        uname = f"@{top_streak_user[1]}" if top_streak_user[1] != "بدون يوزر" else "بدون يوزر"
        report += f"🏆 <b>الأعلى بالقراءات:</b> {uname} (<code>{top_streak_user[0]}</code>) بـ <b>{top_streak_val}</b> يوم\n\n"
    if top_cycle_user and top_cycle_val >= 0:
        uname = f"@{top_cycle_user[1]}" if top_cycle_user[1] != "بدون يوزر" else "بدون يوزر"
        report += f"🥇 <b>الأعلى بالدورات:</b> {uname} (<code>{top_cycle_user[0]}</code>) بـ <b>{top_cycle_val}</b> دورة\n\n"
        
    report += "📋 <b>تفاصيل المشتركين:</b>\n"
    
    for uid, uinfo in data.items():
        if isinstance(uinfo, dict):
            uname = f"@{uinfo.get('username')}" if uinfo.get('username') else "بدون يوزر"
            report += (
                f"• <b>اليوزر:</b> {uname}\n"
                f"  └ <b>الآيدي:</b> <code>{uid}</code>\n"
                f"  └ <b>القراءات:</b> <code>{streak}/40</code> يوم\n"
                f"  └ <b>الدورات:</b> <code>{cycles}</code> دورة\n\n"
            )
        
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⚙️ التحكم بالعدادات", callback_data="admin_control"))
    
    bot.send_message(message.chat.id, report, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['test'])
def test_send_cmd(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    data = load_data()
    date_info = get_dates()
    now = datetime.now(TZ_BAGHDAD)
    time_12h = now.strftime("%I:%M %p")
    
    for uid, uinfo in data.items():
        if uinfo.get("active"):
            try:
                bot.send_audio(int(uid), audio=AUDIO_URL, caption="✨ <b>[اختبار] هذا دعاء العهد صوتياً</b>", parse_mode="HTML")
            except Exception as e:
                print(f"خطأ في إرسال الصوت للمستخدم {uid}: {e}")

            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("سجل قرأت الدعاء هذا اليوم 📖", callback_data="mark_read"))
            
            msg = (
                f" <blockquote>[🧪رسالة اختبار سريعة - تنتهي خلال 30 ثانية]</blockquote>\n"
                f"<blockquote>{DUAA_TEXT}</blockquote>\n\n"
                f"📅 <b>التاريخ:</b> {date_info}\n"
                f"⏰ <b>الوقت:</b> {time_12h}\n"
                f"📊 <b>عدد أيام القراءة المتتالية:</b> {uinfo.get('streak', 0)}/40\n"
                f"🔄 <b>عدد دورات القراءة المكتملة:</b> {uinfo.get('cycles', 0)}"
            )
            
            try:
                sent_msg = bot.send_message(int(uid), msg, reply_markup=markup, parse_mode="HTML")
                
                def expire_test_button():
                    import time as t_m
                    t_m.sleep(30)
                    try:
                        closed_markup = InlineKeyboardMarkup()
                        closed_markup.add(InlineKeyboardButton("❌ انتهى وقت التسجيل (اختبار)", callback_data="expired"))
                        bot.edit_message_reply_markup(int(uid), sent_msg.message_id, reply_markup=closed_markup)
                    except:
                        pass
                threading.Thread(target=expire_test_button, daemon=True).start()
                
            except Exception as e:
                print(f"خطأ في إرسال رسالة الاختبار لـ {uid}: {e}")
                
    bot.reply_to(message, "✅ تم إرسال رسالة الاختبار الصوتية والنصية لجميع المشتركين الفاعلين (ستقفل الأزرار تلقائياً بعد دقيقة)!")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = str(call.from_user.id)
    data = load_data()
    
    if user_id not in data:
        data[user_id] = {
            "active": True,
            "streak": 0,
            "cycles": 0,
            "last_read_date": "",
            "today_sent": False
        }
        update_user_field(user_id, data[user_id])

    if call.data == "expired":
        bot.answer_callback_query(call.id, " انتهى وقت التسجيل الخاص بهذه الجلسة!", show_alert=True)
        return

    if call.data == "toggle_active":
        data[user_id]["active"] = not data[user_id]["active"]
        update_user_field(user_id, data[user_id])
        
        status = "تم تفعيل التذكير بنجاح! 🔔" if data[user_id]["active"] else "تم إيقاف التذكير 🔕"
        bot.answer_callback_query(call.id, status, show_alert=True)
        
        btn_text = "🔕 إيقاف التفعيل" if data[user_id]["active"] else "🔔 تفعيل التذكير اليومي"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(btn_text, callback_data="toggle_active"))
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "mark_read":
        now = datetime.now(TZ_BAGHDAD)
        today_str = now.strftime("%Y-%m-%d")
        
        user = data[user_id]
        if user.get("last_read_date") == today_str:
            bot.answer_callback_query(call.id, "لقد قمت بتسجيل قراءة اليوم بالفعل! ✨", show_alert=True)
            return

        user["streak"] = user.get("streak", 0) + 1
        user["last_read_date"] = today_str
        
        msg_suffix = ""
        if user["streak"] >= 40:
            user["cycles"] = user.get("cycles", 0) + 1
            user["streak"] = 0
            msg_suffix = f"\n\n <blockquote>🎉مبروك! تم إكمال 40 يوماً بنجاح وتم بدء دورة جديدة!</blockquote>\nعدد دوراتك الان: {user['cycles']}"

        update_user_field(user_id, user)
        
        date_info = get_dates()
        time_12h = now.strftime("%I:%M %p")
        
        updated_msg = (
            f"✨ <blockquote>تم تسجيل القراءة بنجاح ✨</blockquote>\n\n"
            f"📅 <b>التاريخ:</b> {date_info}\n"
            f"⏰ <b>الوقت:</b> {time_12h}\n"
            f"📊 <b>عدد أيام القراءة المتتالية:</b> {user['streak']}/40\n"
            f"🔄 <b>عدد دورات القراءة المكتملة:</b> {user['cycles']}\n\n"
            f"استمر على هذا الدعاء تقبل الله طاعاتكم . \n"
            f" <blockquote>{msg_suffix}</blockquote>"
        )
        
        closed_markup = InlineKeyboardMarkup()
        closed_markup.add(InlineKeyboardButton("✅ تم تسجيل القراءة بنجاح 📖", callback_data="expired"))
        
        try:
            bot.edit_message_text(updated_msg, call.message.chat.id, call.message.message_id, reply_markup=closed_markup, parse_mode="HTML")
        except:
            pass
            
        bot.answer_callback_query(call.id, "تم تسجيل قراءتك بنجاح! 🤲")

def daily_scheduler():
    import time as t_module
    while True:
        now = datetime.now(TZ_BAGHDAD)
        today_str = now.strftime("%Y-%m-%d")
        
        if now.hour == 5 and now.minute == 00:
            data = load_data()
            date_info = get_dates()
            time_12h = now.strftime("%I:%M %p")
            send_occurred = False
            
            for uid, uinfo in data.items():
                if uinfo.get("active"):
                    if uinfo.get("last_sent_date") == today_str:
                        continue
                        
                    send_occurred = True
                    try:
                        bot.send_audio(int(uid), audio=AUDIO_URL, caption="✨ <blockquote>هذا دعاء العهد صوتياً اذا كانت لديك اي كلمة لا تعرف نطقها</blockquote>", parse_mode="HTML")
                    except Exception as e:
                        print(f"تعذر إرسال الصوت لـ {uid}: {e}")

                    markup = InlineKeyboardMarkup()
                    markup.add(InlineKeyboardButton("سجل قرأت الدعاء هذا اليوم 📖", callback_data="mark_read"))
                    
                    msg = (
                        f"{DUAA_TEXT}\n\n"
                        f" <blockquote>التاريخ:</blockquote> {date_info}\n"
                        f"<b>الوقت:</b> {time_12h}\n"
                        f"<blockquote> عدد أيام القراءة المتتالية: {uinfo.get('streak', 0)}/40 </blockquote> \n"
                        f"<blockquote>عدد دورات القراءة المكتملة: {uinfo.get('cycles', 0)}</blockquote>"
                    )
                    
                    try:
                        sent_msg = bot.send_message(int(uid), msg, reply_markup=markup, parse_mode="HTML")
                        uinfo["last_msg_id"] = sent_msg.message_id
                        uinfo["last_sent_date"] = today_str
                        update_user_field(uid, uinfo)
                    except Exception as e:
                        print(f"تعذر إرسال النص لـ {uid}: {e}")
                        
            if send_occurred:
                t_module.sleep(3)

        if now.hour == 10 and now.minute == 58:
            data = load_data()
            reset_occurred = False
            
            for uid, uinfo in data.items():
                if uinfo.get("active"):
                    if uinfo.get("last_reset_date") == today_str:
                        continue
                        
                    if uinfo.get("last_read_date") != today_str:
                        reset_occurred = True
                        
                        if uinfo.get("streak", 0) > 0:
                            uinfo["streak"] = 0
                            
                        uinfo["last_reset_date"] = today_str
                        update_user_field(uid, uinfo)
                        
                        if uinfo.get("last_msg_id"):
                            try:
                                expired_markup = InlineKeyboardMarkup()
                                expired_markup.add(InlineKeyboardButton("❌ انتهى وقت التسجيل وتم قفل الزر", callback_data="expired"))
                                bot.edit_message_reply_markup(int(uid), uinfo["last_msg_id"], reply_markup=expired_markup)
                            except Exception as ex:
                                print(f"تعذر قفل زر الرسالة لـ {uid}: {ex}")

                        try:
                            bot.send_message(
                                int(uid), 
                                "⚠️ <b>انتهى الوقت المحدد (11:00 AM) ولم تقم بتسجيل قراءة دعاء العهد اليوم. تم تصفير العداد!</b>", 
                                parse_mode="HTML"
                            )
                        except Exception as e:
                            print(f"خطأ في إرسال إشعار التصفير لـ {uid}: {e}")
                            
            if reset_occurred:
                t_module.sleep(60)

        t_module.sleep(15)

threading.Thread(target=daily_scheduler, daemon=True).start()
print("البوت يعمل بكفاءة الآن وقاعدة البيانات مربطوة بـ Firebase...")
bot.infinity_polling()