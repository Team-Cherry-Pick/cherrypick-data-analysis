from cherrypick_data_analysis.data_analysis.analysis.eda_analysis import *
from cherrypick_data_analysis.data_analysis.component.graph import *


def statistics(params : dict) :
    tab1, tab2, tab3, tab4 = st.tabs(["활동량", "유저", "게시글", "댓글"])
    with tab1 :
        activity_metric(params)
    with tab2 :
        user_metric(params)

def activity_metric(params : dict) :

    with st.expander("Explanation") :
        st.html(
        """
            PPOMPPU는 2005년 핫딜게시판을 개시하여 2000년대 이후 최근 월 4000건의 게시물 수를 보임.<br>
            FMKOREA는 2018년 핫딜게시판을 개시하여 2020년 이후 성장하여 최근 2000건의 게시물 수를 보임.<br>
            <br>
            23.12 기점으로 하락세 접어들었다가 다시 상승 중.<br>
            23.12 FMKOREA 천안문 사태 : <a href="https://gall.dcinside.com/mgallery/board/view/?id=fm1&no=7685" target="_blank">천안문 사태</a> <br>
            <br>
            전체적으로 PPOMPPU와 FMKOREA는 비슷한 모양을 그리는 양상을 띰.<br>
            이에 대한 가설로, <br>
            1. 멀티 유저    : 같은 유저가 두 사이트 모두 올리는 것.<br>
            2. 한정된 핫딜 : 하루에 올라오는 핫딜 양은 한정되어 있기 때문.<br>
            3. 핫딜 도둑질 : 각 사이트의 핫딜을 주고 받기 때문.<br>
            <br>
            게시물은 PPOMPPU가, 조회수는 FMKOREA가 앞서는 양상을 띰.<br>
            PPOMPPU 는 2005년 개시한 핫딜의 원조격 게시판이고,<br>
            FMKOREA 는 원체 사이트 자체 유저 수가 많은 것이 원인으로 추정. (정말 내 추정)<br>
        """)

    trend_of_post_graph(params)
    trend_of_views_graph(params)

def user_metric(params : dict) :
    with st.expander("Explanation") :
        st.html(
            """
                잠드는 새벽 시간을 제외하면 글이 골고루 올라오는 편이다.<br>
                가장 많은 글이 올라오는 시간대는 00시, 10시, 11시로, 17시 순.<br>
                재밌는 점은 23시와 00시의 게시글 수 차이가 매우 크다는 점. <br>
            """)

    deal_posts_by_hour(params)

    selected_graphs = st.multiselect(
        "WHAT GRAPH ?",
        options=["유저 누적 기여도 그래프"],
        default=[]
    )

    if  "유저 누적 기여도 그래프" in selected_graphs :
        with st.expander("Explanation"):
            st.html(
                """
                        분석에 앞서 상위 소비자 그룹에서 상위 공급자 그룹과 겹치는 유저가 다수 보임. <br>
                        공급자가 본인의 게시물에 댓글을 다는 케이스를 배제해야할 듯 함.<br>

                        게시물의 경우 상위 10%의 활동량을 가진 유저가 67%의 게시물을 올림.<br>
                        댓글의 경우 상위 10%의 유저가 70%의 댓글을 달았음.<br><br>

                        최상위 유저들이 대부분의 비중을 가진 양상.<br><br>

                        조금 비약하자면 공급자 / 소비자 그래프 라고도 생각할 수 있음. <br>
                """)
        col1, col2 = st.columns(2)
        with col1 :
            plot_pareto_post_distribution(params)
        with col2 :
            plot_pareto_comment_distribution(params)

def deal_metric(params : dict) :
    "asdf"