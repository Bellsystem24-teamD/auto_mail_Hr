import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time

# --- 1. CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="HR Tech - Bell24 Recruitment", page_icon="🚀", layout="wide")

# --- CSS SỬA LỖI MÀU CHỮ (FIX DARK MODE) ---
st.markdown("""
<style>
    /* Tiêu đề chính */
    .main-title {
        font-size: 30px; 
        font-weight: 800;
        background: linear-gradient(90deg, #0056b3, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 20px;
    }

    /* KHUNG JOB - BẮT BUỘC NỀN TRẮNG CHỮ ĐEN */
    .job-card {
        padding: 25px;
        background-color: white !important;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }
    
    /* QUAN TRỌNG: Ép buộc mọi chữ bên trong .job-card thành màu đen xám */
    .job-card, .job-card p, .job-card span, .job-card b, .job-card div, .job-card h3 {
        color: #333333 !important;
    }

    /* Nút bấm */
    div.stButton > button {
        background: linear-gradient(90deg, #0056b3, #004494);
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        height: 55px;
        width: 100%;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    div.stButton > button:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- DỮ LIỆU JOB ---
JOB_DATABASE = {
    "BIDV - NV Tư vấn Khách hàng": {
        "title": "Chuyên viên Tư vấn CSKH (Dự án BIDV)",
        "salary": "7.000.000đ - 8.000.000đ",
        "location": "Tòa nhà 545 Nguyễn Văn Cừ, Long Biên, Hà Nội",
        "time": "Giờ hành chính (Nghỉ Chủ Nhật & Lễ)",
        "benefit": "Không áp doanh số, Đào tạo bài bản, Đóng BHXH Full",
        "color": "#006d75", "bg_color": "#e0f7fa"
    },
    "MB Bank - CSKH (Không sale)": {
        "title": "Chuyên viên Hỗ trợ Khách hàng MB Bank",
        "salary": "7.000.000đ - 9.000.000đ ++",
        "location": "Tòa nhà MBBank, 21 Cát Linh, Đống Đa, Hà Nội",
        "time": "Xoay ca linh hoạt (Nghỉ 1 ngày/tuần)",
        "benefit": "Hỗ trợ 1.000.000đ đào tạo, Môi trường Bank chuyên nghiệp",
        "color": "#10358e", "bg_color": "#e8eaf6"
    },
    "TPBank - CSKH Full-time": {
        "title": "Nhân viên CSKH TPBank (Inbound)",
        "salary": "7.000.000đ – 9.000.000đ + Thưởng nóng",
        "location": "44 Lê Ngọc Hân / 155 Đội Cấn / Khu Ngoại giao đoàn",
        "time": "Xoay ca (07h00 – 22h00), 6 ngày/tuần",
        "benefit": "Hỗ trợ tài chính đào tạo, Du lịch hàng năm",
        "color": "#762483", "bg_color": "#f3e5f5"
    },
    "TPBank - CSKH Part-time": {
        "title": "Nhân viên Hỗ trợ TPBank (Part-time)",
        "salary": "3.000.000₫ – 5.000.000đ (Việc làm thêm)",
        "location": "Lựa chọn: 44 Lê Ngọc Hân / 155 Đội Cấn / Khu Ngoại giao đoàn",
        "time": "Ca tối: 17h-21h hoặc 18h-22h (Phù hợp sinh viên)",
        "benefit": "Hỗ trợ 120k/ngày đào tạo, Cơ hội lên chính thức",
        "color": "#762483", "bg_color": "#f3e5f5"
    },
    "LPBank - CSKH": {
        "title": "Chuyên viên CSKH LPBank",
        "salary": "7.000.000đ – 9.000.000đ/tháng",
        "location": "135 Xã Đàn, Phường Kim Liên, Hà Nội",
        "time": "Xoay ca (Có ca đêm), nghỉ 1 ngày/tuần",
        "benefit": "Hỗ trợ 100k/ngày đào tạo, Thưởng nóng, Du lịch",
        "color": "#ffad00", "bg_color": "#fff8e1"
    },
    "VETC - Tổng đài viên Giao thông": {
        "title": "Nhân viên CSKH Tổng đài VETC",
        "salary": "7.300.000vnđ (Lương cứng + KPI)",
        "location": "Số 7-9 đường Nguyễn Văn Linh, Long Biên, Hà Nội",
        "time": "Xoay ca (Có trực đêm), nghỉ 1 ngày/tuần",
        "benefit": "Hỗ trợ 100k/ngày đào tạo, Không bán hàng",
        "color": "#008744", "bg_color": "#e8f5e9"
    },
    "UOB - Tư vấn Dịch vụ Thẻ": {
        "title": "Chuyên viên Tư vấn Tài chính - UOB",
        "salary": "15.000.000đ - 20.000.000đ ++",
        "location": "1A Vũ Phạm Hàm, Trung Hòa, Cầu Giấy, Hà Nội",
        "time": "Giờ hành chính (T2-T6), Nghỉ T7 CN",
        "benefit": "Đào tạo 5 ngày có hỗ trợ, Lộ trình thăng tiến rõ ràng",
        "color": "#0b2363", "bg_color": "#e3f2fd"
    },
    "UOB - Thực tập sinh Telesales": {
        "title": "Thực tập sinh Tài chính - UOB",
        "salary": "Trợ cấp 2.000.000đ + Thưởng",
        "location": "Số 2A Vũ Phạm Hàm, Cầu Giấy, Hà Nội",
        "time": "Full-time (8h30 – 17h30, T2 – T6)",
        "benefit": "Hỗ trợ dấu mộc thực tập, Đào tạo bài bản",
        "color": "#0b2363", "bg_color": "#e3f2fd"
    }
}

# --- HEADER ---
st.markdown('<div class="main-title">🚀 BELL SYSTEM24 RECRUITMENT TOOL</div>', unsafe_allow_html=True)
st.divider()

# --- SIDEBAR: CẤU HÌNH ---
with st.sidebar:
    st.header("⚙️ CÀI ĐẶT")
    st.caption("Phiên bản của Trường Vũ - Update 09/12/2025")
    
    st.subheader("1. Server Mail")
    email_provider = st.selectbox("Chọn loại mail:", ["Gmail / G-Suite", "Outlook / Microsoft 365"])
    
    email_gui = st.text_input("Email gửi:", placeholder="example@bs24.vn")
    mat_khau = st.text_input("Mật khẩu:", type="password", help="Gmail dùng App Password. Outlook dùng mật khẩu đăng nhập.")
    contact_info = st.text_input("Chữ ký (Tên - SĐT):", value="Mr Mến - 09xx.xxx.xxx")

    st.subheader("2. Chọn Job & Loại Thư")
    selected_job_name = st.selectbox("Vị trí tuyển dụng:", list(JOB_DATABASE.keys()))
    job_info = JOB_DATABASE[selected_job_name] 

    email_type = st.radio("Loại Email:", ["Mời Ứng Tuyển", "Mời Phỏng Vấn"])

    link_jd, interview_time, interview_loc, interview_note = "", "", "", ""

    if email_type == "Mời Ứng Tuyển":
        link_jd = st.text_input("Link JD (nếu có):", placeholder="https://...")
    else: 
        st.info("📅 Nhập lịch phỏng vấn:")
        interview_time = st.text_input("Thời gian:", "09:00 Sáng, Thứ ... ngày ...")
        interview_loc = st.text_input("Địa điểm:", value=job_info['location'])
        interview_note = st.text_area("Ghi chú:", "Mang theo CV bản cứng + CCCD.")
    
    st.subheader("3. Dữ liệu Ứng viên")
    mode = st.radio("Nguồn dữ liệu:", ["Excel Upload", "Nhập tay"])
    
    df = None
    if mode == "Excel Upload":
        uploaded_file = st.file_uploader("Chọn file Excel", type=['xlsx'])
        if uploaded_file: 
            try:
                df = pd.read_excel(uploaded_file)
            except Exception as e:
                st.error(f"Lỗi đọc file Excel: {e}")
    else:
        col1, col2 = st.columns(2)
        manual_name = col1.text_input("Tên:")
        manual_email = col2.text_input("Email:")
        if manual_name and manual_email:
            df = pd.DataFrame({'Ten': [manual_name], 'Email': [manual_email]})

    st.subheader("4. Ảnh Banner")
    uploaded_banner = st.file_uploader("Ảnh đầu thư (Tùy chọn)", type=['png', 'jpg', 'jpeg'])

# --- HÀM TẠO HTML ---
def create_html(email_type, name, job, contact, jd_link, time_pv, loc_pv, note_pv):
    color = job.get('color', '#0056b3')
    bg = job.get('bg_color', '#f8f9fa')
    
    # CSS inline để đảm bảo email gửi đi không bị lỗi màu
    base_style = "font-family:Arial,sans-serif;font-size:14px;color:#333;line-height:1.6;"
    
    content_body = ""
    title_header = ""
    
    if email_type == "Mời Ứng Tuyển":
        title_header = f"Cơ hội việc làm: {job['title']}"
        btn_jd = ""
        if jd_link:
            btn_jd = f'<div style="text-align:center;margin:20px;"><a href="{jd_link}" style="background:{color};color:white;padding:10px 20px;text-decoration:none;border-radius:20px;font-weight:bold;">Xem chi tiết JD</a></div>'
        
        content_body = f"""
        <p style="{base_style}">Hồ sơ của bạn rất ấn tượng. Mời bạn tham khảo vị trí này:</p>
        <h3 style="color:{color};">{job['title']}</h3>
        <div style="background:{bg};padding:15px;border-left:5px solid {color};border-radius:5px;">
            <p style="{base_style}"><b>💰 Lương:</b> {job['salary']}</p>
            <p style="{base_style}"><b>📍 Địa điểm:</b> {job['location']}</p>
            <p style="{base_style}"><b>⏰ Thời gian:</b> {job['time']}</p>
            <p style="{base_style}"><b>🎁 Quyền lợi:</b> {job['benefit']}</p>
        </div>
        {btn_jd}
        """
    else:
        title_header = f"THƯ MỜI PHỎNG VẤN - {job['title']}"
        content_body = f"""
        <p style="{base_style}">Chúc mừng bạn! Hồ sơ của bạn đã được thông qua. Mời bạn tham gia phỏng vấn:</p>
        <div style="text-align:center;margin:20px;"><span style="background:{color};color:white;padding:10px 20px;border-radius:5px;font-weight:bold;">THƯ MỜI PHỎNG VẤN</span></div>
        <div style="background:{bg};padding:15px;border-left:5px solid {color};border-radius:5px;">
            <p style="{base_style}"><b>📅 Thời gian:</b> <span style="color:red;font-weight:bold;">{time_pv}</span></p>
            <p style="{base_style}"><b>📍 Địa điểm:</b> {loc_pv}</p>
            <p style="{base_style}"><b>📝 Lưu ý:</b> {note_pv}</p>
        </div>
        <p style="{base_style}">Vui lòng Reply hoặc nhắn tin Zalo để xác nhận tham gia!</p>
        """

    html = f"""
    <html><body style="{base_style} background-color:white;">
        <div style="max-width:600px;margin:0 auto;border:1px solid #ddd;padding:20px;border-radius:10px;">
            <img src="cid:banner" style="width:100%;border-radius:5px;margin-bottom:20px;display:block;" alt="">
            <p style="{base_style}">Chào bạn <b>{name}</b>,</p>
            <p style="{base_style}">Mình là <b>{contact.split('-')[0].strip()}</b> từ <b>Bell System24 Vietnam</b>.</p>
            {content_body}
            <div style="border:1px dashed {color};padding:10px;text-align:center;margin-top:20px;border-radius:5px;">
                <p style="margin:0;color:#666;">Liên hệ hỗ trợ:</p>
                <p style="margin:5px 0;font-size:18px;font-weight:bold;color:{color};">📞 {contact}</p>
            </div>
        </div>
    </body></html>
    """
    return html, title_header

# --- GIAO DIỆN CHÍNH ---
col_left, col_right = st.columns([1.5, 1])

col_name = None
col_email = None

if df is not None:
    for c in df.columns:
        if any(x in c.lower() for x in ['tên', 'ten', 'name']): col_name = c
        if any(x in c.lower() for x in ['mail', 'email']): col_email = c

with col_left:
    # HIỂN THỊ CARD JOB (SỬ DỤNG STYLE INLINE ĐỂ CHẮC CHẮN MÀU ĐEN)
    st.markdown(f"""
    <div class="job-card" style="border-left: 5px solid {job_info['color']}; color: #333333 !important;">
        <h3 style="color:{job_info['color']} !important; margin:0;">{job_info['title']}</h3>
        <p style="margin:10px 0 5px 0; color: #333333 !important;"><b>💰 Lương:</b> {job_info['salary']}</p>
        <p style="margin:0; color: #333333 !important;"><b>📍 Địa điểm:</b> {job_info['location']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🚀 Gửi Email")
    
    ready_to_send = False
    if df is not None:
        if col_name and col_email:
            st.success(f"✅ Đã tải {len(df)} dòng dữ liệu.")
            ready_to_send = True
        else:
            st.error("⚠️ File Excel thiếu cột 'Tên' hoặc 'Email'.")

    if st.button(f"GỬI NGAY ({email_provider})"):
        if not ready_to_send:
            st.warning("⚠️ Chưa có dữ liệu để gửi!")
        elif not email_gui or not mat_khau:
            st.warning("⚠️ Vui lòng nhập Email và Mật khẩu ở cột bên trái!")
        else:
            status_area = st.empty()
            progress_bar = st.progress(0)
            
            try:
                server = None
                if "Gmail" in email_provider:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                else:
                    server = smtplib.SMTP('smtp.office365.com', 587)
                
                server.starttls()
                server.login(email_gui, mat_khau)
                
                count = 0
                for i, row in df.iterrows():
                    name = str(row[col_name])
                    email = str(row[col_email])
                    
                    if pd.isna(email) or "@" not in email: continue
                    
                    status_area.text(f"📨 Đang gửi tới: {name}...")
                    
                    html_content, subject_text = create_html(
                        email_type, name, job_info, contact_info, 
                        link_jd, interview_time, interview_loc, interview_note
                    )
                    
                    msg = MIMEMultipart('related')
                    msg['From'] = f"Bell24 Tuyển Dụng <{email_gui}>"
                    msg['To'] = email
                    msg['Subject'] = subject_text
                    
                    msg_alt = MIMEMultipart('alternative')
                    msg.attach(msg_alt)
                    msg_alt.attach(MIMEText(html_content, 'html'))
                    
                    if uploaded_banner:
                        uploaded_banner.seek(0)
                        img = MIMEImage(uploaded_banner.read())
                        img.add_header('Content-ID', '<banner>')
                        msg.attach(img)
                    
                    server.sendmail(email_gui, email, msg.as_string())
                    count += 1
                    progress_bar.progress((i + 1) / len(df))
                    
                    time.sleep(1 if "Outlook" in email_provider else 0.5)
                
                server.quit()
                status_area.success(f"🎉 Đã gửi thành công {count} email!")
                st.balloons()
                
            except smtplib.SMTPAuthenticationError:
                st.error("❌ LỖI ĐĂNG NHẬP: Sai Email hoặc Mật khẩu!")
                if "Outlook" in email_provider:
                    st.info("💡 Với Outlook: Liên hệ IT mở quyền 'SMTP Auth' nếu bị chặn.")
                else:
                    st.info("💡 Với Gmail: Phải dùng 'Mật khẩu ứng dụng' (App Password).")
            except Exception as e:
                st.error(f"❌ Lỗi: {e}")

with col_right:
    st.caption("📝 XEM TRƯỚC EMAIL")
    preview_html, _ = create_html(
        email_type, "[Tên Ứng Viên]", job_info, contact_info, 
        link_jd, interview_time, interview_loc, interview_note
    )
    st.components.v1.html(preview_html, height=600, scrolling=True)
