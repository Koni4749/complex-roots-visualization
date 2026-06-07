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

tab1, tab2, tab3 = st.tabs(["🧩 1. 기하학의 모순", "🌐 2. 3D 복소 공간 (현대의 해법)", "📜 3. 허수의 역사와 스토리텔링"])

with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("정사각형의 넓이로 방정식 풀기")
        st.markdown(r"""
        고대 수학자들은 이차방정식을 풀 때 대수학(수식)이 아닌 **도형의 넓이**를 사용했습니다.
        
        1. 파란색 사각형은 우리가 구해야 할 미지의 넓이 $x^2$입니다.
        2. 양옆의 초록색 직사각형 2개는 각각 $x \times y$의 넓이를 가집니다. (합치면 $2xy$)
        3. 여기까지의 넓이 합($x^2 + 2xy$)은 우변으로 넘긴 **$-c$** 와 같습니다.
        """)
        
        st.info(f"**현재 $x^2 + 2xy$ 의 넓이 = {-c_val:.1f}**")
        
        st.markdown(r"""
        빈 모서리를 채워 완전한 정사각형을 만들려면, 한 변이 $y$인 **노란색 정사각형($y^2$)**이 필요합니다.
        양변에 $y^2$을 더해주면, 완성된 가장 큰 정사각형의 넓이는 다음과 같습니다.
        
        $$(x + y)^2 = y^2 - c$$
        """)
        
    with col2:
        # Plotly를 이용한 2D 도형 시각화
        fig2d = go.Figure()
        
        # 시각적 비율을 위한 고정 변수 (x를 10이라 가정하고 그림)
        vis_x = 10
        vis_y = y_val * 2 # 시각적으로 y값을 맵핑
        
        # 도형 크기 변화를 체감할 수 있도록 축의 최대 범위를 고정합니다.
        fixed_max_dim = 10 + (5.0 * 2) + 2 
        
        # 투명한 점을 양 끝에 찍어서 Plotly가 자동으로 축 범위를 넉넉하게 잡도록 강제합니다.
        fig2d.add_trace(go.Scatter(
            x=[-1, fixed_max_dim], y=[-1, fixed_max_dim], mode="markers", 
            marker=dict(color="rgba(0,0,0,0)"), showlegend=False, hoverinfo="skip"
        ))
        
        # 1. x^2 사각형 (파란색)
        fig2d.add_shape(type="rect", x0=0, y0=0, x1=vis_x, y1=vis_x,
                        fillcolor="rgba(31, 119, 180, 0.7)", line=dict(color="black", width=2))
        fig2d.add_annotation(x=vis_x/2, y=vis_x/2, text="<b>x²</b>", showarrow=False, font=dict(size=22, color="white"))
        
        # 2. xy 직사각형 1 (오른쪽, 초록색)
        fig2d.add_shape(type="rect", x0=vis_x, y0=0, x1=vis_x+vis_y, y1=vis_x,
                        fillcolor="rgba(44, 160, 44, 0.7)", line=dict(color="black", width=2))
        fig2d.add_annotation(x=vis_x+vis_y/2, y=vis_x/2, text=f"<b>xy</b><br>= {y_val:.1f}x", showarrow=False, font=dict(size=16, color="white"))
        
        # 3. xy 직사각형 2 (위쪽, 초록색)
        fig2d.add_shape(type="rect", x0=0, y0=vis_x, x1=vis_x, y1=vis_x+vis_y,
                        fillcolor="rgba(44, 160, 44, 0.7)", line=dict(color="black", width=2))
        fig2d.add_annotation(x=vis_x/2, y=vis_x+vis_y/2, text=f"<b>xy</b><br>= {y_val:.1f}x", showarrow=False, font=dict(size=16, color="white"))
        
        # 4. y^2 정사각형 (우측 상단 빈칸 채우기, 노란색)
        fig2d.add_shape(type="rect", x0=vis_x, y0=vis_x, x1=vis_x+vis_y, y1=vis_x+vis_y,
                        fillcolor="rgba(255, 127, 14, 0.7)", line=dict(color="black", width=2))
        fig2d.add_annotation(x=vis_x+vis_y/2, y=vis_x+vis_y/2, text=f"<b>y²</b><br>= {y_val**2:.2f}", showarrow=False, font=dict(size=16, color="white"))

        # ★ 사용자의 요청: 음수 넓이가 나오는 것을 명시적으로 그래프 위에 표시
        title_text = f"완성된 전체 넓이 (x + {y_val:.1f})² = {area_large_square:.2f}"
        title_color = "red" if area_large_square < 0 else "blue"
        fig2d.add_annotation(
            x=(vis_x+vis_y)/2, y=fixed_max_dim - 1, 
            text=f"<b>{title_text}</b>", 
            showarrow=False, font=dict(size=20, color=title_color)
        )

        fig2d.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="y", scaleratio=1, range=[-1, fixed_max_dim]),
            yaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-1, fixed_max_dim]),
            margin=dict(l=10, r=10, t=10, b=10), height=400, plot_bgcolor="white"
        )
        
        st.plotly_chart(fig2d, use_container_width=True)
        
    st.markdown("---")
    
    # 핵심 로직 시각화: 넓이가 음수인지 판별
    if area_large_square < 0:
        st.error(f"⚠️ **기하학적 모순 발생!** 완성된 큰 정사각형의 넓이가 **{area_large_square:.2f}** 입니다.")
        st.markdown(f"""
        ### 현실의 기하학 붕괴
        위의 도형을 보세요. 가장 바깥쪽을 감싸는 **커다란 정사각형의 넓이가 `{area_large_square:.2f}` (음수)**로 계산되었습니다.
        
        현실(실수 평면)에서 **어떤 도형의 넓이가 0보다 작을 수는 없습니다.**
        수학자들은 이 지점에서 벽에 부딪혔습니다. 하지만 이 불가능해 보이는 음수의 넓이를 뚫고 나가기 위해 **'허수(Imaginary Number)'**라는 새로운 차원을 도입하게 됩니다.
        """)
    else:
        st.success(f"✅ 완성된 큰 정사각형의 넓이가 **{area_large_square:.2f}** (양수) 입니다. 정상적으로 실수 범위에서 길이를 구할 수 있습니다.")

with tab2:
    st.subheader("3D 복소 공간 시각화 (현대의 해법)")
    st.markdown("""
    음수가 되어버린 넓이(2D에서의 모순)를 해결하기 위해, 현대 수학은 **허수 축(Imaginary Axis)**을 하나 더 그립니다.
    2D 평면에서는 넓이가 음수가 되어 막혀버렸던 그래프가, 3D 복소 공간에서는 말안장 모양을 그리며 바닥($y=0$)을 통과해 마침내 해를 만들어냅니다.
    """)
    
    # 3D 그리드 생성 (실수부 u, 허수부 v)
    u = np.linspace(-6, 6, 60)
    v = np.linspace(-6, 6, 60)
    U, V = np.meshgrid(u, v)
    
    # 복소함수 f(z) = (u+vi)^2 + b(u+vi) + c 의 실수부 전개
    Z_real = (U**2 - V**2) + b * U + c_val
    
    fig3d = go.Figure()
    
    # 1. 3D Surface (함수의 실수부) - 말안장 모양
    fig3d.add_trace(go.Surface(
        x=U, y=V, z=Z_real, colorscale='Viridis', opacity=0.85, 
        name='Re(f(z))', showscale=False
    ))
    
    # 2. y=0 평면 (높이가 0인 바닥 평면)
    fig3d.add_trace(go.Surface(
        x=U, y=V, z=np.zeros_like(Z_real), 
        colorscale='Reds' if area_large_square < 0 else 'Greys', 
        opacity=0.5 if area_large_square < 0 else 0.4, 
        showscale=False, name='높이=0 평면'
    ))
    
    # 3. 근 표시 (Scatter3d)
    if area_large_square < 0:
        real_part = -b / 2
        imag_part = np.sqrt(-D) / 2
        rx = [real_part, real_part]
        ry = [imag_part, -imag_part]
    else:
        r1 = (-b + np.sqrt(max(0, D))) / 2
        r2 = (-b - np.sqrt(max(0, D))) / 2
        rx = [r1, r2]
        ry = [0, 0]
        
    rz = [0, 0]
    
    fig3d.add_trace(go.Scatter3d(
        x=rx, y=ry, z=rz, mode='markers',
        marker=dict(size=10, color='red', symbol='circle', line=dict(color='white', width=2)),
        name='방정식의 해'
    ))
    
    fig3d.update_layout(
        scene=dict(
            xaxis_title='실수축 (Real)', yaxis_title='허수축 (Imaginary)', zaxis_title='높이 ( f(z)의 실수부 )',
            xaxis=dict(range=[-6, 6]), yaxis=dict(range=[-6, 6]), zaxis=dict(range=[-30, 50]),
            camera=dict(eye=dict(x=1.5, y=-1.5, z=0.8))
        ),
        margin=dict(l=0, r=0, b=0, t=0), height=600
    )
    st.plotly_chart(fig3d, use_container_width=True)

with tab3:
    st.subheader("📜 허수, 쓸모없는 상상에서 우주의 언어가 되기까지")
    st.markdown("""
    수학은 본래 땅을 측량하고 별자리를 관측하며, 상업의 이윤을 기록하는 등 **현실 세상을 표현하기 위해** 시작되었습니다. 
    그러던 중 현실 세계와는 동떨어진, 불가능해 보이는 문제가 발생합니다. 바로 **'허수(Imaginary Number)'**의 등장입니다.

    ---

    ### 1. 목숨을 건 수학 배틀과 기하학의 한계
    1500년대 이탈리아 르네상스 시절, 수학자들은 대학의 교수직과 생계를 걸고 치열한 **'수학 배틀'**을 벌였습니다. 
    당시 가장 큰 난제는 수천 년간 풀리지 않던 **'3차 방정식'**이었습니다. 타르탈리아(Tartaglia)와 카르다노(Cardano) 같은 수학자들은 이 방정식을 수식이 아닌, 우리가 1번 탭에서 했던 것처럼 **정육면체의 부피를 쪼개고 합치는 '기하학'**으로 접근했습니다.

    ### 2. "음수의 넓이"라는 치명적 모순
    하지만 방정식을 푸는 과정에서 기하학적 역설이 발생합니다. 정답(실근)을 구하려면, 계산 중간에 반드시 **'음수의 넓이(부피)'**를 가진 도형을 더해줘야만 했던 것입니다.
    현실에서 넓이나 부피가 0보다 작은 도형은 존재할 수 없습니다. 따라서 어떤 수를 제곱해서 음수가 나오는 수, 즉 음수의 제곱근($\sqrt{-1}$)은 오랫동안 쓸모없는 궤변으로 여겨졌습니다.

    ### 3. 모순을 끌어안은 타협, 복소수의 탄생
    이때 수학자 라파엘 봄벨리(Bombelli)가 기발한 타협안을 제시합니다. 
    > *"음수의 넓이라는 말도 안 되는 수가 계산 중간에 잠시 존재했다가, 마지막에 서로 상쇄되어 사라진다고 가정해보자."*
    
    그는 현실에 없는 가상의 숫자를 도구로 사용했고, 이를 통해 3차 방정식의 완벽한 실근을 구해냅니다. 이 순간부터 수학은 눈에 보이는 기하학의 한계를 벗어나, 허수를 새로운 수의 체계로 받아들이기 시작했습니다.

    ### 4. 차원의 확장: 허수는 '회전'이다
    허수 $i$는 단순히 존재하지 않는 가짜 숫자가 아닙니다.
    수직선(실수축) 위의 숫자 1에 $i$를 곱하면 허수 $i$가 되고, 한 번 더 $i$를 곱하면 -1이 됩니다. 즉, 허수 $i$를 곱한다는 것은 복소평면 위에서 **90도씩 회전하는 기하학적 움직임**을 의미합니다. 허수의 도입으로 수학은 1차원의 선에서 2차원의 평면으로 시야가 확장되었습니다.

    ### 5. 400년 후, 우주의 비밀을 푸는 열쇠가 되다
    허수가 처음 등장하고 약 400년이 지난 1925년, 물리학자 에르빈 슈뢰딩거(Schrödinger)는 원자와 전자 같은 양자 입자의 움직임을 설명하는 **파동 방정식**을 만듭니다. 놀랍게도 우주를 구성하는 가장 작은 단위를 설명하는 이 절대적인 물리 법칙에는 허수 $i$가 핵심으로 들어가 있었습니다.

    물리학자 프리먼 다이슨은 이렇게 말했습니다.
    > *"슈뢰딩거가 방정식에 $\sqrt{-1}$을 넣었더니 갑자기 모든 것이 이해되었다. 루트 -1은 자연이 실수가 아닌 복소수로 작동한다는 것을 의미한다. 이 발견은 모두에게 완전히 놀라운 일이었다."*

    현실의 넓이를 구하기 위해 만들어졌던 수학이, 상상 속의 숫자를 거쳐 결국 다시 **우주의 가장 깊은 현실을 증명해 내는 근본 언어**가 된 것입니다.
    """)
