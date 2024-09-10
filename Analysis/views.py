from django.http import JsonResponse
from django.shortcuts import render

from Analysis.models import loldata

from Analysis.models import hero_statistics

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
from django.views.generic import ListView

from Analysis import models

from django import forms
# views.py
from django.shortcuts import render

from Analysis.forms import WizardForm
from Analysis.models import hero_statistics
# views.py
from django.shortcuts import render
from Analysis.models import hero_statistics





def index(request):
    hero_statistic = models.hero_statistics
    hero_stats = hero_statistic.objects.all()
    hero_data_dict = {}
    for stat in hero_stats:
        hero_name = stat.hero
        if hero_name in hero_data_dict:
            hero_data_dict[hero_name]['games_played'] += stat.games_played
            hero_data_dict[hero_name]['gold'] += stat.gold
            hero_data_dict[hero_name]['cs'] += stat.cs
            hero_data_dict[hero_name]['ban'] += stat.ban
            hero_data_dict[hero_name]['ban_count'] += 1
        else:
            hero_data_dict[hero_name] = {
                'games_played': stat.games_played,
                'gold': stat.gold,
                'cs': stat.cs,
                'ban': stat.ban,
                'ban_count': 1
            }
    for hero_name, data in hero_data_dict.items():
        data['average_ban_rate'] = data['ban'] / data['ban_count']

    most_ban_hero = max(hero_data_dict, key=lambda x: hero_data_dict[x]['average_ban_rate'])
    most_ban_rate = round(hero_data_dict[most_ban_hero]['average_ban_rate'], 2)

    # 找到登场次数最多的英雄
    most_played_hero = max(hero_data_dict, key=lambda x: hero_data_dict[x]['games_played'])
    most_played_games = hero_data_dict[most_played_hero]['games_played']

    # 找到获得最多金币的英雄
    most_gold_hero = max(hero_data_dict, key=lambda x: hero_data_dict[x]['gold'])
    most_gold_amount = hero_data_dict[most_gold_hero]['gold']
    #cs
    most_cs_hero = max(hero_data_dict, key=lambda x: hero_data_dict[x]['cs'])
    most_cs_amount = int(hero_data_dict[most_cs_hero]['cs'])
    #top7

    hero_winrate_dict = {}
    for stat in hero_stats:
        hero_name = stat.hero
        if stat.games_played > 0:
            winrate = (stat.win/3 / stat.games_played)  * 100   # 计算胜率百分比
        else:
            winrate = 0

        hero_winrate_dict[hero_name] = winrate

    # 按照胜率排序并获取前7个英雄
    top_7_heroes = sorted(hero_winrate_dict.items(), key=lambda x: x[1], reverse=True)[:7]

    # 提取英雄名称和胜率
    top_7_hero_names = [hero[0] for hero in top_7_heroes]
    top_7_winrates = [hero[1] for hero in top_7_heroes]





    hero_statistics = hero_statistic.objects.all().order_by('-games_played')[:10]

    # 获取所有英雄数据
    for stat in hero_statistics:
        if stat.pick > 0:
            stat.popularity = stat.pick
        else:
            stat.popularity = 0  # 避免除以零的情况



    return render(request, 'index.html', {
        'hero_statistics': hero_statistics,
        'most_played_hero': most_played_hero,
        'most_played_games': most_played_games,
        'most_gold_hero': most_gold_hero,
        'most_gold_amount': most_gold_amount,
        'most_cs_hero': most_cs_hero,
        'most_cs_amount': most_cs_amount
        ,'most_ban_hero': most_ban_hero,
        'most_ban_rate': most_ban_rate,
        'top_7_hero_names': top_7_hero_names,
        'top_7_winrates': top_7_winrates
         ,
    })









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
    # 查询 queue_type 为 'aram' 的所有英雄数据
    all_heroes = hero_statistics.objects.filter(queue_type='aram')

    # 计算每个英雄的出场总数
    hero_stats = {}
    for hero in all_heroes:
        if hero.hero in hero_stats:
            hero_stats[hero.hero] += hero.games_played
        else:
            hero_stats[hero.hero] = hero.games_played

    # 计算总出场次数
    total_games = sum(hero_stats.values())

    # 过滤出场次数小于10%的英雄，并将其合并为"其他"
    threshold = 0.009
    hero_pie_data = {hero: count for hero, count in hero_stats.items() if count / total_games >= threshold}
    other_count = sum(count for hero, count in hero_stats.items() if count / total_games < threshold)
    if other_count > 0:
        hero_pie_data['其他'] = other_count

    # 提取饼图数据
    pie_labels = list(hero_pie_data.keys())
    pie_data = list(hero_pie_data.values())

    # 查询 tier 为 'aram' 的胜率前7个英雄
    top_heroes = hero_statistics.objects.filter(queue_type='aram').order_by('-win')[:7]
    top_hero_names = [hero.hero for hero in top_heroes]
    top_win_rates = [hero.win for hero in top_heroes]
    top_games_played = [hero.games_played for hero in top_heroes]

    # 将数据传递给模板
    context = {
        'top_hero_names': top_hero_names,
        'top_win_rates': top_win_rates,
        'top_games_played': top_games_played,
        'pie_labels': pie_labels,
        'pie_data': pie_data,
    }
    return render(request, 'bestteam_aram.html', context)







def bestteam_arena(request):

        return render(request, 'bestteam_arena.html')



def bestteam_normal(request):
    if request.method == 'POST':
        # 获取用户提交的数据
        role = request.POST.get('role')

        queue_type = request.POST.get('queue_type')
        tier = request.POST.get('tier')
        remark = request.POST.get('remark')

        # 根据 queue_type 转换为所需格式
        if queue_type == 'solo':
            queue_type = 'ranked'
        else:
            queue_type = 'flex'

        # 查询胜率最高的五位英雄
        print(role, queue_type, tier, remark)
        loldata = models.loldata
        top_heroes = models.loldata.objects.filter(
            role=role,
            tier=tier
        ).order_by('-win')[:5]  # 按照胜率降序排序并取前五个

        # 提取英雄名字
        hero_names = [hero.hero for hero in top_heroes]

        # 返回 JSON 响应

        return JsonResponse({'success': True, 'heroes': hero_names})

    else:
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
