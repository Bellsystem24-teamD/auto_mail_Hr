import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(page_title="Tool Tuyển Dụng Bell24 by_MrMến", page_icon="⚡", layout="wide")

# --- DỮ LIỆU JOB (KÈM MÀU THƯƠNG HIỆU & BG) ---
JOB_DATABASE = {
    "BIDV - NV Tư vấn Khách hàng": {
        "title": "Chuyên viên Tư vấn CSKH (Dự án BIDV)",
        "salary": "7.000.000đ - 8.000.000đ (Thu nhập ổn định)",
        "location": "Tòa nhà 545 Nguyễn Văn Cừ, Long Biên, Hà Nội",
        "time": "Giờ hành chính (Nghỉ Chủ Nhật & Lễ)",
        "benefit": "Không áp doanh số, Đào tạo bài bản, Đóng BHXH Full",
        "color": "#006d75", "bg_color": "#e0f7fa" # Xanh Teal BIDV
    },
    "MB Bank - CSKH (Không sale)": {
        "title": "Chuyên viên Hỗ trợ Khách hàng MB Bank",
        "salary": "7.000.000đ - 9.000.000đ ++",
        "location": "Tòa nhà MBBank, 21 Cát Linh, Đống Đa, Hà Nội",
        "time": "Xoay ca linh hoạt (Nghỉ 1 ngày/tuần)",
        "benefit": "Hỗ trợ 1.000.000đ đào tạo, Môi trường Bank chuyên nghiệp",
        "color": "#10358e", "bg_color": "#e8eaf6" # Xanh dương MB
    },
    "TPBank - CSKH Full-time": {
        "title": "Nhân viên CSKH TPBank (Inbound)",
        "salary": "7.000.000đ – 9.000.000đ + Thưởng nóng",
        "location": "44 Lê Ngọc Hân / 155 Đội Cấn / Ngoại Giao Đoàn",
        "time": "Xoay ca (07h00 – 22h00), 6 ngày/tuần",
        "benefit": "Hỗ trợ tài chính đào tạo, Du lịch hàng năm",
        "color": "#762483", "bg_color": "#f3e5f5" # Tím TPBank
    },
    "TPBank - CSKH Part-time": {
        "title": "Nhân viên Hỗ trợ TPBank (Part-time)",
        "salary": "3.000.000₫ – 5.000.000đ (Việc làm thêm)",
        "location": "Lựa chọn: 44 Lê Ngọc Hân / 155 Đội Cấn",
        "time": "Ca tối: 17h-21h hoặc 18h-22h (Phù hợp sinh viên)",
        "benefit": "Hỗ trợ 120k/ngày đào tạo, Cơ hội lên chính thức",
        "color": "#762483", "bg_color": "#f3e5f5"
    },
    "LPBank - CSKH": {
        "title": "Chuyên viên CSKH Ngân hàng Lộc Phát (LPBank)",
        "salary": "7.000.000đ – 9.000.000đ/tháng",
        "location": "135 Xã Đàn, Phường Kim Liên, Hà Nội",
        "time": "Xoay ca (Có ca đêm), nghỉ 1 ngày/tuần",
        "benefit": "Hỗ trợ 100k/ngày đào tạo, Thưởng nóng, Du lịch",
        "color": "#ffad00", "bg_color": "#fff8e1" # Vàng Cam LPBank
    },
    "VETC - Tổng đài viên Giao thông": {
        "title": "Nhân viên CSKH Tổng đài VETC",
        "salary": "7.300.000vnđ (Lương cứng + KPI)",
        "location": "Số 7-9 đường Nguyễn Văn Linh, Long Biên, Hà Nội",
        "time": "Xoay ca (Có trực đêm), nghỉ 1 ngày/tuần",
        "benefit": "Hỗ trợ 100k/ngày đào tạo, Không bán hàng",
        "color": "#008744", "bg_color": "#e8f5e9" # Xanh lá VETC
    },
    "UOB - Tư vấn Dịch vụ Thẻ": {
        "title": "Chuyên viên Tư vấn Tài chính - UOB",
        "salary": "15.000.000đ - 20.000.000đ ++ (Lương cao)",
        "location": "1A Vũ Phạm Hàm, Trung Hòa, Cầu Giấy, Hà Nội",
        "time": "Giờ hành chính (T2-T6), Nghỉ T7 CN",
        "benefit": "Đào tạo 5 ngày có hỗ trợ, Lộ trình thăng tiến rõ ràng",
        "color": "#0b2363", "bg_color": "#e3f2fd" # Xanh Navy UOB
    },
    "UOB - Thực tập sinh Telesales": {
        "title": "Thực tập sinh Tài chính - Ngân hàng UOB",
        "salary": "Trợ cấp 2.000.000đ + Thưởng (đến 1.250.000đ)",
        "location": "Số 2A Vũ Phạm Hàm, Cầu Giấy, Hà Nội",
        "time": "Full-time (8h30 – 17h30, T2 – T6)",
        "benefit": "Hỗ trợ dấu mộc thực tập, Đào tạo bài bản, Lên chính thức",
        "color": "#0b2363", "bg_color": "#e3f2fd"
    }
}

st.title("⚡ TOOL TUYỂN DỤNG BELL SYSTEM24_by_MrMến")

# --- CỘT TRÁI: CẤU HÌNH ---
with st.sidebar:
    st.header("1. Email & Liên hệ")
    email_gui = st.text_input("Gmail của bạn", "trantruongvu61@gmail.com")
    mat_khau = st.text_input("Mật khẩu ứng dụng", type="password")
    contact_info = st.text_input("Tên & SĐT Zalo của bạn:", value="Nguyễn Lộc - 0326489852")
    link_jd = st.text_input("Link JD chi tiết (nếu có):", placeholder="Dán link vào đây...")
    
    st.divider()
    st.header("2. Chọn Job & Nhập liệu")
    selected_job_name = st.selectbox("📌 Vị trí tuyển dụng:", list(JOB_DATABASE.keys()))
    job_info = JOB_DATABASE[selected_job_name] 
    
    mode = st.radio("👉 Chế độ:", ["Gửi hàng loạt (Excel)", "Gửi từng người (Nhập tay)"])
    
    df = None
    if mode == "Gửi hàng loạt (Excel)":
        uploaded_file = st.file_uploader("📂 Tải Excel", type=['xlsx'])
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
    else:
        st.caption("Nhập nhanh thông tin dưới đây:")
        manual_name = st.text_input("Họ tên ứng viên:")
        manual_email = st.text_input("Email ứng viên:")
        if manual_name and manual_email:
            df = pd.DataFrame({'Ten': [manual_name], 'Email': [manual_email]})

    st.divider()
    uploaded_banner = st.file_uploader("🖼️ Ảnh Banner (hiện đầu thư)", type=['png', 'jpg', 'jpeg'])

# --- HÀM TẠO HTML EMAIL ---
def create_email_html(name_candidate, job_data, contact, link_jd):
    main_color = job_data.get('color', '#0056b3')
    bg_color = job_data.get('bg_color', '#f8f9fa')

    jd_block = ""
    if link_jd:
        jd_block = f"""
        <div style="margin-top: 20px; text-align: center;">
            <a href="{link_jd}" style="background-color: {main_color}; color: white; padding: 12px 25px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 14px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                📄 XEM CHI TIẾT CÔNG VIỆC
            </a>
            <p style="font-size: 12px; color: #888; margin-top: 10px;">(Hoặc bấm vào đây để xem mô tả đầy đủ)</p>
        </div>
        """

    html = f"""
    <html><body style="font-family: 'Segoe UI', Arial, sans-serif; font-size: 14px; line-height: 1.6; color: #333; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
            <img src="cid:banner" style="width:100%; border-radius: 8px; margin-bottom: 25px; display: block;" alt="Banner">
            <p style="font-size: 16px;">Chào bạn <b>{name_candidate}</b>,</p>
            <p>Mình là <b>{contact.split('-')[0].strip()}</b> từ bộ phận Tuyển dụng <b>Bell System24 Vietnam</b>.</p>
            <p>Hồ sơ của bạn rất ấn tượng và phù hợp với vị trí bên mình đang tìm kiếm. Mình trân trọng mời bạn tham khảo cơ hội này:</p>
            
            <h2 style="color: {main_color}; margin-top: 20px; font-size: 20px; border-bottom: 2px solid {main_color}; display: inline-block; padding-bottom: 5px;">
                {job_data['title']}
            </h2>
            
            <div style="background-color: {bg_color}; border: 1px solid {main_color}30; border-left: 6px solid {main_color}; border-radius: 8px; padding: 20px; margin: 20px 0;">
                <p><b>💰 THU NHẬP:</b> <span style="color: {main_color}; font-weight: 600;">{job_data['salary']}</span></p>
                <p><b>📍 ĐỊA ĐIỂM:</b> {job_data['location']}</p>
                <p><b>⏰ THỜI GIAN:</b> {job_data['time']}</p>
                <p><b>🎁 QUYỀN LỢI:</b> {job_data['benefit']}</p>
            </div>
            
            <p><i>Bell System24 cam kết tuyển dụng trực tiếp và không thu phí.</i></p>
            <p>Để trao đổi nhanh, bạn hãy kết nối Zalo với mình nhé:</p>
            
            <div style="background: #ffffff; border: 2px dashed {main_color}; padding: 15px; border-radius: 8px; text-align: center; margin: 20px 0;">
                <p style="margin: 0; font-size: 14px; color: #555;">Liên hệ trực tiếp HR:</p>
                <p style="margin: 5px 0; font-size: 22px; font-weight: bold; color: {main_color};">📞 {contact}</p>
            </div>
            
            {jd_block}
            
            <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
            <p style="color: #999; font-size: 12px; text-align: center;">Trân trọng,<br>Bộ phận Tuyển dụng Bell System24 Vietnam.</p>
        </div>
    </body></html>
    """
    return html

# --- CỘT PHẢI: XEM TRƯỚC & GỬI ---
col1, col2 = st.columns([2, 1])

# LOGIC TÌM CỘT
col_name, col_email = None, None
if df is not None:
    # Tìm cột thông minh hơn
    possible_names = ['tên', 'ten', 'name', 'họ tên', 'full name', 'ứng viên']
    for c in df.columns:
        if any(p in c.lower() for p in possible_names):
            col_name = c
            break
            
    possible_emails = ['mail', 'email', 'gmail', 'thư']
    for c in df.columns:
        if any(p in c.lower() for p in possible_emails):
            col_email = c
            break

with col1:
    st.subheader("📝 Xem trước")
    preview_content = create_email_html("[Tên Ứng Viên]", job_info, contact_info, link_jd)
    st.components.v1.html(preview_content, height=800, scrolling=True)

with col2:
    st.subheader("🚀 Bảng điều khiển")
    
    is_ready = False
    if df is not None:
        if col_name and col_email:
            st.success(f"✅ Đã nhận diện {len(df)} dòng dữ liệu.")
            is_ready = True
        else:
            st.error("⚠️ File Excel thiếu cột Tên hoặc Email!")
    else:
        st.info("👈 Đang chờ nhập liệu...")

    # NÚT GỬI LUÔN HIỆN (Bấm vào mới check lỗi)
    if st.button("🚀 GỬI EMAIL NGAY (SIÊU TỐC)", type="primary"):
        if not is_ready:
            st.error("❌ Chưa có dữ liệu hoặc file Excel bị lỗi cột.")
        elif not mat_khau:
            st.error("❌ Quên nhập Mật khẩu ứng dụng rồi!")
        else:
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email_gui, mat_khau)
                
                bar = st.progress(0)
                status = st.empty()
                count = 0
                
                for i, row in df.iterrows():
                    name = str(row[col_name])
                    email = str(row[col_email])
                    
                    if pd.isna(email) or email == "nan" or "@" not in email: continue
                    
                    status.text(f"📨 Đang gửi tới: {name}...")
                    
                    msg = MIMEMultipart('related')
                    msg['From'] = f"Bell24 Tuyển Dụng <{email_gui}>"
                    msg['To'] = email
                    msg['Subject'] = f"Cơ hội việc làm: {job_info['title']}"
                    
                    real_html = create_email_html(name, job_info, contact_info, link_jd)
                    msg_alt = MIMEMultipart('alternative')
                    msg.attach(msg_alt)
                    msg_alt.attach(MIMEText(real_html, 'html'))
                    
                    if uploaded_banner:
                        uploaded_banner.seek(0)
                        img = MIMEImage(uploaded_banner.read())
                        img.add_header('Content-ID', '<banner>')
                        msg.attach(img)
                    
                    server.sendmail(email_gui, email, msg.as_string())
                    count += 1
                    bar.progress((i + 1) / len(df))
                    
                    # TỐC ĐỘ CAO: Chỉ nghỉ 0.1 giây
                    time.sleep(0.1) 
                
                server.quit()
                st.success(f"🎉 Đã gửi xong {count} email!")
                st.balloons()
                
            except Exception as e:
                st.error(f"Lỗi: {e}")