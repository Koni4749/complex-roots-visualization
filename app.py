import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- 페이지 설정 ---
st.set_page_config(
    page_title="허수의 기하학적 탄생",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 사이드바: 입력 파라미터 ---
with st.sidebar:
    st.header("⚙️ 방정식 설정")
    st.markdown("도형의 직관적 이해를 위해 $x^2$의 계수는 1로, 일차항은 $2y$로 표현합니다.")
    
    st.divider()
    
    # 슬라이더
    y_val = st.slider("y 값 (직사각형 한 변)", min_value=1.0, max_value=5.0, value=2.0, step=0.5)
    c_val = st.slider("c 값 (상수항)", min_value=-10.0, max_value=20.0, value=5.0, step=0.5)

    b = 2 * y_val
    a = 1.0

    # 완전제곱식 면적 계산: (x + y)^2 = y^2 - c
    area_large_square = (y_val**2) - c_val
    D = b**2 - 4*a*c_val # 판별식
    
    st.divider()
    
    # 실시간 수식 피드백
    st.subheader("현재 방정식")
    st.latex(f"x^2 + {b:.1f}x + {c_val:.1f} = 0")
    
    st.subheader("상태 요약")
    st.metric(label="완성된 정사각형의 넓이 (y² - c)", value=f"{area_large_square:.2f}")

    if area_large_square > 0:
        st.success("🟢 양수 넓이 (서로 다른 두 실근)")
    elif np.isclose(area_large_square, 0):
        st.warning("🟡 넓이 0 (중근)")
    else:
        st.error("🔴 음수 넓이 발생! (서로 다른 두 허근)")


# --- 메인 화면 ---
st.title("📐 기하학으로 보는 허수의 탄생")
st.markdown("""
<div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #1f77b4; margin-bottom: 20px;'>
    <h4 style='margin-top: 0;'>학습 안내</h4>
    과거 수학자들은 이차방정식을 풀 때 <b>'도형의 넓이'</b>를 이용했습니다. <br>
    왼쪽의 슬라이더를 움직여 정사각형의 넓이가 <b>음수</b>가 되는 모순을 만들어보고, 그 한계를 극복하기 위해 등장한 <b>복소평면과 켤레근</b>의 기하학적 의미를 눈으로 확인해 보세요.
</div>
""", unsafe_allow_html=True)

st.latex(rf"\Rightarrow (x + {y_val:.1f})^2 = {area_large_square:.1f}")

# 탭 구성 (불필요한 텍스트 제거 및 직관적 네이밍)
tab1, tab2, tab3 = st.tabs(["🧩 1. 기하학의 모순 (2D 넓이)", "🌐 2. 차원의 확장 (복소평면)", "📜 3. 허수의 역사"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("정사각형 완성하기 (Completing the Square)")
        st.markdown(r"""
        고대 수학자들은 수식이 아닌 도형의 넓이로 방정식을 풀었습니다.
        
        1. 파란색 사각형은 우리가 구해야 할 미지의 넓이 $x^2$ 입니다.
        2. 양옆의 초록색 직사각형 2개는 각각 $x \times y$ 의 넓이를 가집니다.
        3. 여기까지의 넓이 합($x^2 + 2xy$)은 우변으로 넘긴 $-c$ 와 같습니다.
        """)
        
        st.info(f"현재 조각들의 넓이 합 ($x^2 + 2xy$) = {-c_val:.1f}")
        
        st.markdown(r"""
        빈 모서리를 채워 하나의 완전한 정사각형을 만들려면, 한 변이 $y$ 인 노란색 정사각형($y^2$)이 필요합니다.
        양변에 $y^2$ 을 더해주면, 완성된 가장 큰 정사각형의 전체 넓이는 다음과 같이 계산됩니다.
        
        $$(x + y)^2 = y^2 - c$$
        """)
        
    with col2:
        fig2d = go.Figure()
        
        vis_x = 10
        vis_y = y_val * 2
        fixed_max_dim = 10 + (5.0 * 2) + 2 
        
        fig2d.add_trace(go.Scatter(
            x=[-1, fixed_max_dim], y=[-1, fixed_max_dim], mode="markers", 
            marker=dict(color="rgba(0,0,0,0)"), showlegend=False, hoverinfo="skip"
        ))
        
        # 도형 렌더링 (hoverinfo="skip" 추가로 깔끔한 상호작용 유도)
        fig2d.add_shape(type="rect", x0=0, y0=0, x1=vis_x, y1=vis_x,
                        fillcolor="rgba(31, 119, 180, 0.7)", line=dict(color="black", width=2))
        fig2d.add_annotation(x=vis_x/2, y=vis_x/2, text="x²", showarrow=False, font=dict(size=22, color="white"))
        
        fig2d.add_shape(type="rect", x0=vis_x, y0=0, x1=vis_x+vis_y, y1=vis_x,
                        fillcolor="rgba(44, 160, 44, 0.7)", line=dict(color="black", width=2))
        fig2d.add_annotation(x=vis_x+vis_y/2, y=vis_x/2, text=f"xy<br>= {y_val:.1f}x", showarrow=False, font=dict(size=16, color="white"))
        
        fig2d.add_shape(type="rect", x0=0, y0=vis_x, x1=vis_x, y1=vis_x+vis_y,
                        fillcolor="rgba(44, 160, 44, 0.7)", line=dict(color="black", width=2))
        fig2d.add_annotation(x=vis_x/2, y=vis_x+vis_y/2, text=f"xy<br>= {y_val:.1f}x", showarrow=False, font=dict(size=16, color="white"))
        
        fig2d.add_shape(type="rect", x0=vis_x, y0=vis_x, x1=vis_x+vis_y, y1=vis_x+vis_y,
                        fillcolor="rgba(255, 127, 14, 0.7)", line=dict(color="black", width=2))
        fig2d.add_annotation(x=vis_x+vis_y/2, y=vis_x+vis_y/2, text=f"y²<br>= {y_val**2:.2f}", showarrow=False, font=dict(size=16, color="white"))

        # 넓이 결과 텍스트 강조
        title_text = f"완성된 전체 넓이 (x + {y_val:.1f})² = {area_large_square:.2f}"
        title_color = "#d62728" if area_large_square < 0 else "#1f77b4"
        fig2d.add_annotation(
            x=(vis_x+vis_y)/2, y=fixed_max_dim - 0.5, 
            text=f"<b>{title_text}</b>", 
            showarrow=False, font=dict(size=20, color=title_color)
        )

        fig2d.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="y", scaleratio=1, range=[-1, fixed_max_dim]),
            yaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-1, fixed_max_dim]),
            margin=dict(l=10, r=10, t=10, b=10), height=450, plot_bgcolor="white"
        )
        
        st.plotly_chart(fig2d, use_container_width=True)
        
    st.divider()
    
    if area_large_square < 0:
        st.error(f"🚨 기하학적 모순 발생! 완성된 큰 정사각형의 넓이가 {area_large_square:.2f} 입니다.")
        st.markdown(f"""
        ### 현실 기하학의 붕괴
        위의 도형을 확인해 보세요. 가장 바깥쪽을 감싸는 커다란 정사각형의 넓이가 **음수**로 계산되었습니다.
        
        현실(수직선과 실수 평면)에서 어떤 도형의 넓이가 0보다 작을 수는 없습니다.
        수학자들은 이 지점에서 거대한 벽에 부딪혔습니다. 하지만 이 불가능해 보이는 음수의 넓이를 해결하기 위해, 현실의 1차원 수직선을 벗어난 새로운 차원의 수, **허수(Imaginary Number)**를 도입하게 됩니다.
        """)
    else:
        st.success(f"✅ 완성된 큰 정사각형의 넓이가 {area_large_square:.2f} (양수) 입니다. 정상적으로 실수 범위(수직선)에서 길이를 구할 수 있습니다.")

with tab2:
    st.subheader("복소평면: 1차원의 선에서 2차원의 평면으로")
    st.markdown(r"""
    넓이가 양수일 때 방정식의 해는 1차원 수직선(실수축) 위에 얌전히 놓여 있습니다. 
    하지만 넓이가 음수가 되는 순간, 방정식의 해는 갈 곳을 잃고 수직선을 벗어납니다. 그리고 **복소평면(Complex Plane)** 위에서 위아래로 대칭을 이루며 뻗어나가는 **켤레근**의 형태로 새롭게 태어납니다.
    """)
    
    fig_complex = go.Figure()
    axis_range = 10
    real_part = -y_val
    
    # 십자선 (수학적 좌표계 스타일)
    fig_complex.add_hline(y=0, line_width=2, line_color="#333333")
    fig_complex.add_vline(x=0, line_width=2, line_color="#333333")
    
    if area_large_square > 0:
        root_val = np.sqrt(area_large_square)
        r1, r2 = real_part + root_val, real_part - root_val
        
        # 중심점 표시
        fig_complex.add_trace(go.Scatter(
            x=[real_part], y=[0], mode='markers',
            marker=dict(size=8, color='gray', symbol='cross'),
            name='중심축 (-y)', hoverinfo="skip"
        ))
        
        # 실근 표시
        fig_complex.add_trace(go.Scatter(
            x=[r1, r2], y=[0, 0],
            mode='markers+text',
            marker=dict(size=14, color='#1f77b4', line=dict(width=2, color='white')),
            text=[f"x₁ = {r1:.2f}", f"x₂ = {r2:.2f}"],
            textposition="top center",
            textfont=dict(size=14),
            name='실근', hoverinfo="x"
        ))
        st.info("현재 상태: 면적이 양수이므로 해가 가로축(실수축) 위에 두 점으로 존재합니다.")

    elif np.isclose(area_large_square, 0):
        fig_complex.add_trace(go.Scatter(
            x=[real_part], y=[0],
            mode='markers+text',
            marker=dict(size=14, color='#ff7f0e', line=dict(width=2, color='white')),
            text=[f"x = {real_part:.2f} (중근)"],
            textposition="top center",
            textfont=dict(size=14),
            name='중근', hoverinfo="x"
        ))
        st.warning("현재 상태: 면적이 0이므로 가로축(실수축) 위에 중복된 하나의 점으로 존재합니다.")
        
    else:
        imag_part = np.sqrt(-area_large_square)
        
        # 중심점 (실수부)
        fig_complex.add_trace(go.Scatter(
            x=[real_part], y=[0], mode='markers',
            marker=dict(size=8, color='gray', symbol='cross'),
            name='중심축 (실수부)', hoverinfo="skip"
        ))
        
        # 켤레근 점선
        fig_complex.add_trace(go.Scatter(
            x=[real_part, real_part], y=[imag_part, -imag_part],
            mode='lines', line=dict(color='#d62728', width=2, dash='dash'),
            showlegend=False, hoverinfo="skip"
        ))
        
        # 허근 (켤레복소수) 표시
        fig_complex.add_trace(go.Scatter(
            x=[real_part, real_part], y=[imag_part, -imag_part],
            mode='markers+text',
            marker=dict(size=14, color='#d62728', line=dict(width=2, color='white')),
            text=[f"x₁ = {real_part:.2f} + {imag_part:.2f}i", f"x₂ = {real_part:.2f} - {imag_part:.2f}i"],
            textposition=["top center", "bottom center"],
            textfont=dict(size=14),
            name='허근 (켤레근)', hoverinfo="text"
        ))
        st.error("현재 상태: 면적이 음수가 되어 가로축을 벗어났습니다! 세로축(허수축) 방향으로 거울처럼 대칭인 두 점(켤레근)으로 존재합니다.")

    # 모눈종이(Grid) 스타일 적용으로 수학적 미학 강조
    fig_complex.update_layout(
        xaxis=dict(title='실수축 (Real Axis)', range=[-axis_range, axis_range], gridcolor='#e5e5e5', dtick=2),
        yaxis=dict(title='허수축 (Imaginary Axis)', range=[-axis_range, axis_range], gridcolor='#e5e5e5', dtick=2),
        width=700, height=600,
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor="#fafafa"
    )
    
    col_spacer1, col_plot, col_spacer2 = st.columns([1, 3, 1])
    with col_plot:
        st.plotly_chart(fig_complex, use_container_width=True)

with tab3:
    st.subheader("허수, 쓸모없는 상상에서 우주의 언어가 되기까지")
    
    st.markdown("""
    수학은 본래 땅을 측량하고 별자리를 관측하며, 상업의 이윤을 기록하는 등 **현실 세상을 표현하기 위해** 시작되었습니다. 
    그러던 중 현실 세계와는 동떨어진, 불가능해 보이는 문제가 발생합니다. 바로 허수(Imaginary Number)의 등장입니다.
    """)
    
    st.divider()

    st.markdown("""
    #### ⚔️ 1. 목숨을 건 수학 배틀과 기하학의 한계
    1500년대 이탈리아 르네상스 시절, 수학자들은 대학의 교수직과 생계를 걸고 치열한 수학 배틀을 벌였습니다. 
    당시 가장 큰 난제는 수천 년간 풀리지 않던 3차 방정식이었습니다. 타르탈리아와 카르다노 같은 수학자들은 이 방정식을 수식이 아닌, 우리가 1번 탭에서 했던 것처럼 도형의 넓이와 부피를 쪼개고 합치는 **기하학**으로 접근했습니다.

    #### 🧩 2. '음수의 넓이'라는 치명적 모순
    하지만 방정식을 푸는 과정에서 기하학적 역설이 발생합니다. 정답(실근)을 구하려면, 계산 중간에 반드시 **음수의 넓이**를 가진 도형을 더해줘야만 했던 것입니다.
    현실에서 넓이나 부피가 0보다 작은 도형은 존재할 수 없습니다. 따라서 어떤 수를 제곱해서 음수가 나오는 수, 즉 음수의 제곱근은 오랫동안 쓸모없는 궤변으로 여겨졌습니다.

    #### 🤝 3. 모순을 끌어안은 타협, 복소수의 탄생
    이때 수학자 라파엘 봄벨리가 기발한 타협안을 제시합니다. 
    
    > *"음수의 넓이라는 말도 안 되는 수가 계산 중간에 잠시 존재했다가, 마지막에 서로 상쇄되어 사라진다고 가정해보자."*
    
    그는 현실에 없는 가상의 숫자를 도구로 사용했고, 이를 통해 3차 방정식의 완벽한 실근을 구해냅니다. 이 순간부터 수학은 눈에 보이는 기하학의 한계를 벗어나, 허수를 새로운 수의 체계로 받아들이기 시작했습니다.

    #### 🔄 4. 차원의 확장: 허수는 '회전'이다
    허수 $i$는 단순히 존재하지 않는 가짜 숫자가 아닙니다.
    수직선(실수축) 위의 숫자 1에 $i$를 곱하면 허수 $i$가 되고, 한 번 더 $i$를 곱하면 -1이 됩니다. 즉, 허수 $i$를 곱한다는 것은 복소평면 위에서 **90도씩 회전하는 기하학적 움직임**을 의미합니다. 허수의 도입으로 수학은 1차원의 선에서 2차원의 평면으로 시야가 확장되었습니다.

    #### 🌌 5. 400년 후, 우주의 비밀을 푸는 열쇠가 되다
    허수가 처음 등장하고 약 400년이 지난 1925년, 물리학자 에르빈 슈뢰딩거는 원자와 전자 같은 양자 입자의 움직임을 설명하는 파동 방정식을 만듭니다. 놀랍게도 우주를 구성하는 가장 작은 단위를 설명하는 이 절대적인 물리 법칙에는 허수 $i$가 핵심으로 들어가 있었습니다.

    물리학자 프리먼 다이슨은 이렇게 회고했습니다.
    
    > *"슈뢰딩거가 방정식에 루트 -1을 넣었더니 갑자기 모든 것이 이해되었다. 루트 -1은 자연이 실수가 아닌 복소수로 작동한다는 것을 의미한다. 이 발견은 모두에게 완전히 놀라운 일이었다."*

    현실의 넓이를 구하기 위해 만들어졌던 수학이, 상상 속의 숫자를 거쳐 결국 다시 **우주의 가장 깊은 현실을 증명해 내는 근본 언어**가 된 것입니다.
    """)
