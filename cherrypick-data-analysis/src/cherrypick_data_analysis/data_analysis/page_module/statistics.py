from cherrypick_data_analysis.data_analysis.analysis.eda_analysis import *
from cherrypick_data_analysis.data_analysis.component.graph import *


def statistics(start_date, end_date, selected_sites) :

    monthly = get_monthly_deal_post_trend(selected_sites, start_date, end_date)
    line_chart("🗓️ 딜 콘텐츠 월간 발생량 추이", monthly)

    monthly_view = get_monthly_deal_view_trend(selected_sites, start_date, end_date)
    line_chart("😉 월별 총 딜 조회수 수 추이", monthly_view)

    size = get_marcket_value_over_time()
    line_chart("💹 월별 시장 규모 추이", size)

    category = get_post_count_by_category()
    bar_chart("📊 카테고리 별 딜 수", category)
