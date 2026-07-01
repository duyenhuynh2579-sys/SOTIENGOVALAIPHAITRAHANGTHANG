import streamlit as st
import pandas as pd
st.image("logo.jpg.jpg", width=200)

# Cấu hình trang ứng dụng
st.set_page_config(page_title="Công Cụ Tính Khoản Vay Công Ty", layout="wide")

st.title("📊 ĐỀ TÀI 02: TÍNH SỐ TIỀN GỐC VÀ LÃI PHẢI TRẢ HÀNG THÁNG KHI VAY VỐN NGÂN HÀNG")
st.write("")
st.markdown("---")

# ==========================================
# 1. THANH BÊN (SIDEBAR) - NHẬP DỮ LIỆU ĐẦU VÀO
# ==========================================
st.sidebar.header("📂 Thông tin khoản vay")

# Nhập các thông tin cơ bản dựa theo cấu trúc file tài liệu
muc_dich = st.sidebar.selectbox("Mục đích vay", ["Mua ô tô", "Mua nhà", "Kinh doanh", "Tiêu dùng"])
san_pham = st.sidebar.selectbox("Loại  vay", ["Vay thế chấp", "Vay tín chấp"])

P = st.sidebar.number_input("Số tiền vay (P) - VNĐ", min_value=1000000, value=300000000, step=10000000)
n = st.sidebar.number_input("Thời hạn vay (n) - Tháng", min_value=1, value=36, step=1)
r_nam = st.sidebar.number_input("Lãi suất (%/năm)", min_value=0.0, value=10.0, step=0.1)

phuong_thuc = st.sidebar.radio(
    "Phương thức trả nợ",
    ["Trả góp cố định (Annuity)", "Dư nợ giảm dần"]
)

# Đổi lãi suất năm thành lãi suất tháng (dạng thập phân)
r = (r_nam / 100) / 12

# ==========================================
# 2. LOGIC TÍNH TOÁN (BACKEND)
# ==========================================
lich_trinh = []

if phuong_thuc == "Trả góp cố định (Annuity)":
    # Tính số tiền trả cố định hàng tháng (E)
    if r > 0:
        E = P * (r * (1 + r)**n) / ((1 + r)**n - 1)
    else:
        E = P / n
        
    du_no_goc = P
    tong_lai_ky_han = 0
    
    for i in range(1, n + 1):
        tien_lai = du_no_goc * r
        tien_goc = E - tien_lai
        du_no_cuoi = du_no_goc - tien_goc
        tong_lai_ky_han += tien_lai
        
        lich_trinh.append({
            "Kỳ trả nợ (Tháng)": i,
            "Dư nợ đầu kỳ (VNĐ)": round(du_no_goc),
            "Gốc phải trả (VNĐ)": round(tien_goc),
            "Lãi phải trả (VNĐ)": round(tien_lai),
            "Tổng trả hàng tháng (VNĐ)": round(E),
            "Dư nợ cuối kỳ (VNĐ)": round(max(0, du_no_cuoi))
        })
        du_no_goc = du_no_cuoi
        
    goc_thang_dau = lich_trinh[0]["Gốc phải trả (VNĐ)"]
    lai_thang_dau = lich_trinh[0]["Lãi phải trả (VNĐ)"]
    tong_thang_dau = lich_trinh[0]["Tổng trả hàng tháng (VNĐ)"]
    tong_phai_tra = P + tong_lai_ky_han

else:  # Dư nợ giảm dần
    goc_hang_thang = P / n
    du_no_goc = P
    tong_lai_ky_han = 0
    
    for i in range(1, n + 1):
        tien_lai = du_no_goc * r
        tong_hang_thang = goc_hang_thang + tien_lai
        du_no_cuoi = du_no_goc - goc_hang_thang
        tong_lai_ky_han += tien_lai
        
        lich_trinh.append({
            "Kỳ trả nợ (Tháng)": i,
            "Dư nợ đầu kỳ (VNĐ)": round(du_no_goc),
            "Gốc phải trả (VNĐ)": round(goc_hang_thang),
            "Lãi phải trả (VNĐ)": round(tien_lai),
            "Tổng trả hàng tháng (VNĐ)": round(tong_hang_thang),
            "Dư nợ cuối kỳ (VNĐ)": round(max(0, du_no_cuoi))
        })
        du_no_goc = du_no_cuoi

    goc_thang_dau = lich_trinh[0]["Gốc phải trả (VNĐ)"]
    lai_thang_dau = lich_trinh[0]["Lãi phải trả (VNĐ)"]
    tong_thang_dau = lich_trinh[0]["Tổng trả hàng tháng (VNĐ)"]
    tong_phai_tra = P + tong_lai_ky_han

# Chuyển đổi lịch trình thành DataFrame để hiển thị trên UI
df_lich_trinh = pd.DataFrame(lich_trinh)

# ==========================================
# 3. HIỂN THỊ KẾT QUẢ TRÊN GIAO DIỆN (FRONTEND)
# ==========================================

# Khối thông tin tổng quan của hồ sơ vay
col1, col2, col3 = st.columns(3)
with col1:
    st.info(f"**🎯 Mục đích:** {muc_dich}")
with col2:
    st.info(f"**Loại hình:** {san_pham}")
with col3:
    st.info(f"**🛠️ Phương thức:** {phuong_thuc}")

st.subheader("📌 Kết quả phân tích chi tiết")

# Các chỉ số Key Metrics cốt lõi (Gốc, Lãi tháng đầu, Tổng tiền)
m1, m2, m3 = st.columns(3)
m1.metric(label="Gốc trả tháng đầu tiên", value=f"{goc_thang_dau:,.0f} VNĐ")
m2.metric(label="Lãi trả tháng đầu tiên", value=f"{lai_thang_dau:,.0f} VNĐ")
m3.metric(label="Tổng số tiền trả tháng đầu", value=f"{tong_thang_dau:,.0f} VNĐ")

m4, m5, m6 = st.columns(3)
m4.metric(label="Số tiền gốc vay ban đầu", value=f"{P:,.0f} VNĐ")
m5.metric(label="Tổng tiền lãi phải trả", value=f"{tong_lai_ky_han:,.0f} VNĐ")
m6.metric(label="Tổng tiền phải trả (Gốc + Lãi)", value=f"{tong_phai_tra:,.0f} VNĐ", delta=f"Lãi chiếm {(tong_lai_ky_han/tong_phai_tra)*100:.1f}%")

st.markdown("---")

# Biểu đồ trực quan hóa xu hướng trả nợ hàng tháng
st.subheader("📈 Biểu đồ xu hướng thanh toán")
chart_data = df_lich_trinh[["Kỳ trả nợ (Tháng)", "Gốc phải trả (VNĐ)", "Lãi phải trả (VNĐ)"]]

# Sử dụng màu Đỏ Nhạt (#E57373) và Xanh Dương Nhạt (#64B5F6)
st.area_chart(
    chart_data.set_index("Kỳ trả nợ (Tháng)"),
    color=["#E57373", "#64B5F6"]
)
# Bảng lịch trình thanh toán chi tiết từng tháng
st.subheader("📋 Lịch trình trả nợ chi tiết qua từng kỳ")
st.dataframe(df_lich_trinh.style.format({
    "Dư nợ đầu kỳ (VNĐ)": "{:,.0f}",
    "Gốc phải trả (VNĐ)": "{:,.0f}",
    "Lãi phải trả (VNĐ)": "{:,.0f}",
    "Tổng trả hàng tháng (VNĐ)": "{:,.0f}",
    "Dư nợ cuối kỳ (VNĐ)": "{:,.0f}"
}), use_container_width=True)

# Nút tải dữ liệu về máy (Export Excel/CSV)
csv = df_lich_trinh.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label="📥 Tải lịch trình trả nợ về máy (CSV)",
    data=csv,
    file_name=f"lich_tra_no_{muc_dich}_{phuong_thuc}.csv",
    mime="text/csv",
)
