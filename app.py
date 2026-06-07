import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- 페이지 설정 ---
st.set_page_config(
    page_title="허수의 기하학적 이해 🌌",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 사이드바: 입력 파라미터 ---
st.sidebar.header("⚙️ 이차방정식 계수 설정")
st.sidebar.markdown(r"방정식 형태: **$ax^2 + bx + c = 0$**")

# 슬라이더를 통한 계수 조절
a = st.sidebar.slider("계수 a (이차항)", min_value=1.0, max_value=5.0, value=1.0, step=0.1)
b = st.sidebar.slider("계수 b (일차항)", min_value=-10.0, max_value=10.0, value=2.0, step=0.1)
c = st.sidebar.slider("계수 c (상수항)", min_value=-10.0, max_value=20.0, value=5.0, step=0.1)

# 판별식 계산
D = b**2 - 4*a*c

# 근의 계산 로직
st.sidebar.markdown("---")
st.sidebar.subheader("📊 판별식 및 근의 상태")
st.sidebar.metric(label="판별식 D (b² - 4ac)", value=f"{D:.2f}")

roots = []  # (실수부, 허수부) 형태로 저장
if D > 0:
    root_status = "🟢 서로 다른 두 실근"
    r1 = (-b + np.sqrt(D)) / (2*a)
    r2 = (-b - np.sqrt(D)) / (2*a)
    roots_str = f"x₁ = {r1:.2f}\nx₂ = {r2:.2f}"
    roots = [(r1, 0), (r2, 0)]
elif np.isclose(D, 0):
    root_status = "🟡 중근 (실근)"
    r1 = -b / (2*a)
    roots_str = f"x = {r1:.2f}"
    roots = [(r1, 0)]
else:
    root_status = "🔴 서로 다른 두 허근"
    real_part = -b / (2*a)
    imag_part = np.sqrt(-D) / (2*a)
    roots_str = f"x₁ = {real_part:.2f} + {imag_part:.2f}i\nx₂ = {real_part:.2f} - {imag_part:.2f}i"
    roots = [(real_part, imag_part), (real_part, -imag_part)]

st.sidebar.info(f"**상태:** {root_status}\n\n**해(Roots):**\n\n{roots_str}")

# --- 메인 화면 ---
st.title("이차방정식과 허수의 기하학적 이해 🌌")
st.markdown(f"현재 설정된 방정식: &nbsp;&nbsp; **${a:.1f}x^2 + {b:.1f}x + {c:.1f} = 0$**")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["📉 2D 실함수 그래프", "🌐 3D 복소 공간 시각화", "📖 수학적 원리 설명"])

with tab1:
    st.subheader("2D 실수 평면에서의 그래프")
    st.markdown("보통의 실수 평면에서는 판별식 $D < 0$일 때 그래프가 $x$축과 만나지 않아 **근이 없다**고 배웁니다.")
    
    # 2D x 값 범위 설정
    x_2d = np.linspace(-10, 10, 400)
    y_2d = a * x_2d**2 + b * x_2d + c
    
    fig2d = go.Figure()
    # 이차함수 곡선
    fig2d.add_trace(go.Scatter(x=x_2d, y=y_2d, mode='lines', name=f'{a}x² + {b}x + {c}', line=dict(color='#1f77b4', width=3)))
    # x축 (y=0)
    fig2d.add_trace(go.Scatter(x=x_2d, y=np.zeros_like(x_2d), mode='lines', name='y=0 (x축)', line=dict(color='black', dash='dash')))
    
    # 실근일 경우 교점 표시
    if D >= 0:
        for r_real, _ in roots:
            fig2d.add_trace(go.Scatter(x=[r_real], y=[0], mode='markers', name='실근',
                                       marker=dict(size=12, color='red', line=dict(color='white', width=2))))
            
    fig2d.update_layout(
        xaxis_title="x (실수)",
        yaxis_title="y",
        hovermode="x unified",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    # y축 범위 고정으로 시각적 안정감 부여
    fig2d.update_yaxes(range=[-10, 50])
    st.plotly_chart(fig2d, use_container_width=True)


with tab2:
    st.subheader("3D 복소 공간에서의 시각화 (말안장 곡면)")
    st.markdown("""
    $x$축을 **복소수($z = u + vi$)**로 확장해 봅시다. 
    가로축은 실수부($u$), 세로축은 허수부($v$), 높이축은 함수 $f(z)$의 **실수부 값**을 나타냅니다.
    마우스를 드래그하여 화면을 이리저리 돌려보세요!
    """)
    
    # 3D 그리드 생성 (실수부 u, 허수부 v)
    u = np.linspace(-6, 6, 60)
    v = np.linspace(-6, 6, 60)
    U, V = np.meshgrid(u, v)
    
    # 복소함수 f(z) = a(u+vi)^2 + b(u+vi) + c 의 실수부 전개
    # Re(f(z)) = a(u^2 - v^2) + bu + c
    Z_real = a * (U**2 - V**2) + b * U + c
    
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
        colorscale='Greys', 
        opacity=0.4, 
        showscale=False, 
        name='높이=0 평면'
    ))
    
    # 3. 근 표시 (Scatter3d)
    rx = [r[0] for r in roots]  # 실수부
    ry = [r[1] for r in roots]  # 허수부
    rz = [0] * len(roots)       # 근에서 함수의 높이는 0
    
    # 허근이든 실근이든 평면과 만나는 점을 붉은색 큰 점으로 표시
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
            camera=dict(eye=dict(x=1.5, y=-1.5, z=0.8)) # 초기 카메라 시점
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=700
    )
    st.plotly_chart(fig3d, use_container_width=True)


with tab3:
    st.subheader("📖 허근은 과연 존재하지 않는 걸까요?")
    st.markdown(r"""
    우리는 흔히 $y = ax^2 + bx + c$ 그래프가 $x$축과 만나지 않으면 **"근이 없다"**라고 말합니다. 
    하지만 엄밀히 말하면 **"실수인 근(실근)이 없다"**는 뜻입니다.

    수학자들은 숫자의 범위를 실수($x$)에서 **복소수($z = u + vi$)**로 확장했습니다.
    이차함수에 복소수 $z$를 대입해 보면 어떻게 될까요?

    ### 1. 차원을 확장하다
    $f(z) = a(u+vi)^2 + b(u+vi) + c$ 를 계산하여 실수 부분만 떼어내면 다음과 같은 식이 됩니다.
    $$ \text{높이} = a(u^2 - v^2) + bu + c $$

    이 식을 가만히 살펴보면 아주 놀라운 사실을 알 수 있습니다.
    - **실수 방향($u$축)**으로는 $+au^2$ 이므로 **아래로 볼록**한 밥그릇 모양(U자)입니다. (2D에서 보던 그 모양입니다.)
    - **허수 방향($v$축)**으로는 $-av^2$ 이므로 **위로 볼록**한 우산 모양(∩자)이 됩니다!

    ### 2. 말안장(Saddle)과 허근의 탄생
    한쪽으로는 위로 올라가고, 다른 쪽으로는 아래로 내려가는 이 기하학적 형태를 **말안장(Saddle)** 구조라고 부릅니다.
    
    **[3D 복소 공간 시각화] 탭**을 다시 확인해 보세요.
    실수축(가로)으로만 보면 붕 떠 있어서 바닥(높이=0)에 닿지 않던 그래프가, 
    **허수축(세로) 방향으로 날개를 펼치면서 아래로 뻗어 내려와 결국 바닥 평면을 뚫고 지나가게 됩니다.**

    이 바닥(높이=0)을 관통하는 **두 개의 점**이 바로 우리가 찾던 **두 허근**입니다!
    
    ### 💡 결론
    허수는 현실에 없는 가짜 숫자가 아닙니다. 단지 우리가 1차원의 선(실수축)만 바라보고 있었기 때문에 보이지 않았을 뿐, 
    **2차원의 평면(복소평면)으로 시야를 넓히면 방정식의 해는 항상 그 자리에 존재하고 있습니다.**
    대수학의 기본 정리(Fundamental Theorem of Algebra)는 이렇게 기하학적으로 아름답게 증명됩니다.
    """)
