from django.shortcuts import render

from Analysis.models import loldata

from Analysis.models import hero_statistics

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def index(request):

    roles = ["weqw","dasd"]
    return render(request,'index.html')
def aram(request):
    query = request.GET.get('search', '')  # 获取搜索框中的输入
    tier = request.GET.get('tier', '').lower()  # 段位

    TIER_TRANSLATION = {
        "master": "超凡大师",
        "grandmaster": "傲世宗师",
        "challenger": "最强王者",
        "diamond": "璀璨钻石",
        "platinum": "华贵铂金",
        "gold": "荣耀黄金",
        "silver": "不屈白银",
        "bronze": "英勇青铜",
        "iron": "坚韧黑铁",
        "emerald": "流光翡翠",
        "all":"综合",
    }

    tier_translated = TIER_TRANSLATION.get(tier, tier)

    data = hero_statistics.objects.filter(queue_type='aram')

    # 根据查询条件进行过滤
    if query:
        data = data.filter(hero__icontains=query)
    if tier_translated:
        # 获取英文段位名称，用于数据库过滤
        tier_en = {v: k for k, v in TIER_TRANSLATION.items()}.get(tier_translated, None)
        if tier_en:
            data = data.filter(tier=tier_en)

    data = list(data.values())
    for item in data:
        item['tier'] = TIER_TRANSLATION.get(item['tier'], item['tier'])
    #分页
    paginator = Paginator(data, 50)  # 每页显示10条数据
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # 对数据进行翻译
    data = list(page_obj.object_list)  # 转换为列表
    for item in data:
        item['tier'] = TIER_TRANSLATION.get(item['tier'], item['tier'])  # 进行翻译

    return render(request, 'aram.html',{
        'hero_statistics':page_obj,
        'query': query,
        'selected_tier': tier,
    })

def arena(request):
    return render(request, 'arena.html')

def bestteam_aram(request):
    return render(request, 'bestteam_aram.html')

def bestteam_arena(request):
    return render(request, 'bestteam_arena.html')

def bestteam_normal(request):
    return render(request, 'bestteam_normal.html')

def bottom(request):
    return render(request, 'bottom.html')

def jungle(request):
    return render(request, 'jungle.html')

def middle(request):
    return render(request, 'middle.html')

def ranked_flex(request):
    return render(request, 'ranked_flex.html')

def ranked_solo(request):
    query = request.GET.get('search', '')  # 获取搜索框中的输入
    tier = request.GET.get('tier', '').lower()     # 段位
    role = request.GET.get('role', '')     # 位置

    TIER_TRANSLATION = {
        "master": "超凡大师",
        "grandmaster": "傲世宗师",
        "challenger": "最强王者",
        "diamond": "璀璨钻石",
        "platinum": "华贵铂金",
        "gold": "荣耀黄金",
        "silver": "不屈白银",
        "bronze": "英勇青铜",
        "iron": "坚韧黑铁",
        "emerald": "流光翡翠",
    }

    tier_translated = TIER_TRANSLATION.get(tier, tier)

    data = loldata.objects.all()


    # 根据查询条件进行过滤
    if query:
        data = data.filter(hero__icontains=query)
    if tier_translated:
        # 获取英文段位名称，用于数据库过滤
        tier_en = {v: k for k, v in TIER_TRANSLATION.items()}.get(tier_translated, None)
        if tier_en:
            data = data.filter(tier=tier_en)
    if role:
        data = data.filter(role=role)

    data = list(data.values())
    for item in data:
        item['tier'] = TIER_TRANSLATION.get(item['tier'], item['tier'])
    #分页
    paginator = Paginator(data, 50)  # 每页显示10条数据
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # 对数据进行翻译
    data = list(page_obj.object_list)  # 转换为列表
    for item in data:
        item['tier'] = TIER_TRANSLATION.get(item['tier'], item['tier'])  # 进行翻译

    return render(request, 'ranked_solo.html', {
        'lol_data': page_obj,
        'query': query,
        'selected_tier': tier,
        'selected_role': role
    })


def support(request):
    return render(request, 'support.html')

def top(request):
    return render(request, 'top.html')
