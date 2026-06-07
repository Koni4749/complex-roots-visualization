import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- 페이지 설정 ---
st.set_page_config(
    page_title="고대 그리스의 도형과 허수 🏛️",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 사이드바: 입력 파라미터 ---
st.sidebar.header("⚙️ 방정식 설정")
st.sidebar.markdown(r"방정식: **$x^2 + 2yx + c = 0$**")
st.sidebar.markdown("(도형의 직관적 이해를 위해 $x^2$의 계수는 1로, 일차항은 $2y$로 표현합니다.)")

# 슬라이더
y_val = st.sidebar.slider("y 값 (직사각형 한 변)", min_value=1.0, max_value=5.0, value=2.0, step=0.5)
c_val = st.sidebar.slider("c 값 (상수항)", min_value=-10.0, max_value=20.0, value=5.0, step=0.5)

b = 2 * y_val
a = 1.0

# 완전제곱식 면적 계산: (x + y)^2 = y^2 - c
area_large_square = (y_val**2) - c_val
D = b**2 - 4*a*c_val # 판별식 (기존 방식 참고용)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 면적 및 근의 상태")
st.sidebar.metric(label="완성된 정사각형의 면적 (y² - c)", value=f"{area_large_square:.2f}")

if area_large_square > 0:
    status = "🟢 양수 면적 (실근 존재)"
    st.sidebar.success(status)
elif np.isclose(area_large_square, 0):
    status = "🟡 면적 0 (중근)"
    st.sidebar.warning(status)
else:
    status = "🔴 음수 면적! (허근 발생)"
    st.sidebar.error(status)


# --- 메인 화면 ---
st.title("🏛️ 기하학으로 보는 허수의 탄생")
st.markdown(f"현재 방정식: &nbsp;&nbsp; **$x^2 + {b:.1f}x + {c_val:.1f} = 0$** &nbsp;&nbsp; $\\rightarrow$ &nbsp;&nbsp; **$x^2 + 2({y_val:.1f})x = {-c_val:.1f}$**")

tab1, tab2 = st.tabs(["🧩 1. 고대 그리스의 정사각형 완성", "🌐 2. 3D 복소 공간 시각화 (현대의 해법)"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("정사각형의 면적으로 방정식 풀기")
        st.markdown(r"""
        고대 수학자들은 이차방정식을 풀 때 대수학(수식)이 아닌 **도형의 넓이**를 사용했습니다.
        
        1. 파란색 사각형은 $x^2$의 넓이를 가집니다.
        2. 양옆의 초록색 직사각형 2개는 각각 $x \times y$의 넓이를 가집니다. (합치면 $2xy$)
        3. 여기까지의 넓이 합($x^2 + 2xy$)은 우변으로 넘긴 **$-c$** 와 같습니다.
        """)
        
        st.info(f"**현재 $x^2 + 2xy$ 의 넓이 = {-c_val:.1f}**")
        
        st.markdown(r"""
        빈 모서리를 채워 완전한 정사각형을 만들려면, 한 변이 $y$인 **노란색 정사각형($y^2$)**이 필요합니다.
        양변에 $y^2$을 더해주면, 완성된 가장 큰 정사각형의 넓이는 다음과 같습니다.
        
        $$ (x + y)^2 = y^2 - c $$
        """)
        
    with col2:
        # Plotly를 이용한 2D 도형 시각화
        fig2d = go.Figure()
        
        # 시각적 비율을 위한 고정 변수 (x를 10이라 가정하고 그림)
        vis_x = 10
        vis_y = y_val * 2 # 시각적으로 y값을 맵핑
        
        # 1. x^2 사각형 (파란색)
        fig2d.add_shape(type="rect", x0=0, y0=0, x1=vis_x, y1=vis_x,
                        fillcolor="rgba(31, 119, 180, 0.7)", line=dict(color="black", width=2))
        fig2d.add_annotation(x=vis_x/2, y=vis_x/2, text="<b>x²</b>", showarrow=False, font=dict(size=20, color="white"))
        
        # 2. xy 직사각형 1 (오른쪽, 초록색)
        fig2d.add_shape(type="rect", x0=vis_x, y0=0, x1=vis_x+vis_y, y1=vis_x,
                        fillcolor="rgba(44, 160, 44, 0.7)", line=dict(color="black", width=2))
        fig2d.add_annotation(x=vis_x+vis_y/2, y=vis_x/2, text="<b>xy</b>", showarrow=False, font=dict(size=16, color="white"))
        
        # 3. xy 직사각형 2 (위쪽, 초록색)
        fig2d.add_shape(type="rect", x0=0, y0=vis_x, x1=vis_x, y1=vis_x+vis_y,
                        fillcolor="rgba(44, 160, 44, 0.7)", line=dict(color="black", width=2))
        fig2d.add_annotation(x=vis_x/2, y=vis_x+vis_y/2, text="<b>xy</b>", showarrow=False, font=dict(size=16, color="white"))
        
        # 4. y^2 정사각형 (우측 상단 빈칸 채우기, 노란색)
        fig2d.add_shape(type="rect", x0=vis_x, y0=vis_x, x1=vis_x+vis_y, y1=vis_x+vis_y,
                        fillcolor="rgba(255, 127, 14, 0.7)", line=dict(color="black", width=2))
        fig2d.add_annotation(x=vis_x+vis_y/2, y=vis_x+vis_y/2, text="<b>y²</b>", showarrow=False, font=dict(size=16, color="white"))

        # 축 및 레이아웃 설정
        fig2d.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="y", scaleratio=1),
            yaxis=dict(showgrid=False, zeroline=False, visible=False),
            margin=dict(l=10, r=10, t=10, b=10),
            height=400,
            plot_bgcolor="white"
        )
        
        st.plotly_chart(fig2d, use_container_width=True)
        
    st.markdown("---")
    
    # 핵심 로직 시각화: 넓이가 음수인지 판별
    if area_large_square < 0:
        st.error(f"⚠️ **모순 발생!** 완성된 큰 정사각형의 넓이가 **{area_large_square:.2f}** 입니다.")
        st.markdown(f"""
        ### 현실의 기하학 붕괴
        계산식에 따르면, 가장 바깥쪽을 감싸는 **커다란 정사각형의 면적이 `{area_large_square:.2f}` (음수)**가 되었습니다.
        
        현실(실수 평면)에서 **어떤 도형의 면적이 0보다 작을 수는 없습니다.**
        같은 맥락에서 어떤 수(길이)를 제곱했는데 음수가 나오는 것도 실수에서는 불가능합니다.
        
        고대인들은 이 지점에서 **"이 방정식은 해가 없다"**고 결론 내렸습니다. 하지만 현대의 우리는 이 불가능해 보이는 음수 면적을 뚫고 나가기 위해 **'허수(Imaginary Number)'**라는 새로운 차원을 도입합니다.
        """)
    else:
        st.success(f"✅ 완성된 큰 정사각형의 넓이가 **{area_large_square:.2f}** (양수) 입니다. 정상적으로 실수 범위에서 길이를 구할 수 있습니다.")

with tab2:
    st.subheader("3D 복소 공간 시각화 (현대의 해법)")
    st.markdown("""
    음수가 되어버린 면적(2D에서의 모순)을 해결하기 위해, 현대 수학은 **허수 축(Imaginary Axis)**을 하나 더 그립니다.
    2D 평면에서는 면적이 음수가 되어 막혀버렸던 그래프가, 3D 복소 공간에서는 말안장 모양을 그리며 바닥($y=0$)을 통과해 해를 만들어냅니다.
    """)
    
    # 3D 그리드 생성 (실수부 u, 허수부 v)
    u = np.linspace(-6, 6, 60)
    v = np.linspace(-6, 6, 60)
    U, V = np.meshgrid(u, v)
    
    # 복소함수 f(z) = (u+vi)^2 + b(u+vi) + c 의 실수부 전개
    # Re(f(z)) = u^2 - v^2 + bu + c
    Z_real = (U**2 - V**2) + b * U + c_val
    
    fig3d = go.Figure()
    
    # 1. 3D Surface (함수의 실수부) - 말안장 모양
    fig3d.add_trace(go.Surface(
        x=U, y=V, z=Z_real, 
        colorscale='Viridis', 
        opacity=0.85, 
        name='Re(f(z))',
        showscale=False
    ))
    
    # 2. y=0 평면 (높이가 0인 바닥 평면)
    fig3d.add_trace(go.Surface(
        x=U, y=V, z=np.zeros_like(Z_real), 
        colorscale='Reds' if area_large_square < 0 else 'Greys', 
        opacity=0.5 if area_large_square < 0 else 0.4, 
        showscale=False, 
        name='높이=0 평면'
    ))
    
    # 3. 근 표시 (Scatter3d)
    if area_large_square < 0:
        # 허근 계산
        real_part = -b / 2
        imag_part = np.sqrt(-D) / 2
        rx = [real_part, real_part]
        ry = [imag_part, -imag_part]
    else:
        # 실근 계산
        r1 = (-b + np.sqrt(max(0, D))) / 2
        r2 = (-b - np.sqrt(max(0, D))) / 2
        rx = [r1, r2]
        ry = [0, 0]
        
    rz = [0, 0]
    
    fig3d.add_trace(go.Scatter3d(
        x=rx, y=ry, z=rz,
        mode='markers',
        marker=dict(size=10, color='red', symbol='circle', line=dict(color='white', width=2)),
        name='방정식의 해'
    ))
    
    fig3d.update_layout(
        scene=dict(
            xaxis_title='실수축 (Real)',
            yaxis_title='허수축 (Imaginary)',
            zaxis_title='높이 ( f(z)의 실수부 )',
            xaxis=dict(range=[-6, 6]),
            yaxis=dict(range=[-6, 6]),
            zaxis=dict(range=[-30, 50]),
            camera=dict(eye=dict(x=1.5, y=-1.5, z=0.8))
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=600
    )
    st.plotly_chart(fig3d, use_container_width=True)
