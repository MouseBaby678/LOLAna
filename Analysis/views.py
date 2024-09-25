from random import random

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
    # cs
    most_cs_hero = max(hero_data_dict, key=lambda x: hero_data_dict[x]['cs'])
    most_cs_amount = int(hero_data_dict[most_cs_hero]['cs'])
    # top7

    hero_winrate_dict = {}
    for stat in hero_stats:
        hero_name = stat.hero
        if stat.games_played > 0:
            winrate = (stat.win / 3 / stat.games_played) * 100  # 计算胜率百分比
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
        , 'most_ban_hero': most_ban_hero,
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
        "all": "综合",
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
    # 分页
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

    return render(request, 'aram.html', {
        'hero_statistics': page_obj,
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
    from django.db.models import Avg
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
        ).order_by('-win')[:10]  # 按照胜率降序排序并取前五个

        # 提取英雄名字
        hero_names = [hero.hero for hero in top_heroes]

        # 记录高低段位的胜率差距
        recommended_heroes = []

        for hero_name in hero_names:
            # 查询该英雄在不同段位的胜率
            win_rates = models.loldata.objects.filter(hero=hero_name).values('tier', 'win')

            # 计算高段位和低段位的胜率
            high_tier_win = \
            win_rates.filter(tier__in=['emerald', 'diamond', 'master', 'grandmaster', 'challenger']).aggregate(
                avg_win=Avg('win'))['avg_win']
            low_tier_win = \
            win_rates.filter(tier__in=['iron', 'bronze', 'silver', 'gold', 'platinum']).aggregate(avg_win=Avg('win'))[
                'avg_win']

            # 标记为难度更高的英雄
            if high_tier_win and low_tier_win and (high_tier_win - low_tier_win) > 0.1:  # 差距大于10%
                recommended_heroes.append({
                    'hero': hero_name,
                    'difficulty': '高'
                })
            else:
                recommended_heroes.append({
                    'hero': hero_name,
                    'difficulty': '普通'
                })

        print(recommended_heroes)

        if remark == '糕手':
            recommended_heroes = [hero for hero in recommended_heroes if hero['difficulty'] != '高']

        recommended_hero_names = [hero['hero'] for hero in recommended_heroes]
        # 返回 JSON 响应
        print(recommended_hero_names)
        return JsonResponse({'success': True, 'heroes': recommended_hero_names})

    else:
        return render(request, 'bestteam_normal.html')


def bottom(request):
    # 获取前五个英雄的名字
    top_heroes = list(
        loldata.objects.filter(role='下路', tier='challenger').order_by('id').values_list('hero', flat=True)[:5])

    # 使用这些英雄名字进行查询
    hero_statistics_data = hero_statistics.objects.filter(
        hero__in=top_heroes,
        tier='all',
        queue_type='ranked'
    )

    # 转换查询集为列表以便处理
    hero_statistics_list = list(hero_statistics_data.values('hero', 'win', 'pick'))

    # 提取数据
    heroes = [item['hero'] for item in hero_statistics_list]
    win_rates = [item['win'] for item in hero_statistics_list]
    pick_rates = [item['pick'] for item in hero_statistics_list]

    # 计算平均值
    avg_cs = hero_statistics_data.aggregate(Avg('cs'))['cs__avg']
    avg_kda = hero_statistics_data.aggregate(Avg('kda'))['kda__avg']
    avg_gold = hero_statistics_data.aggregate(Avg('gold'))['gold__avg']
    avg_games_played = hero_statistics_data.aggregate(Avg('games_played'))['games_played__avg']

    return render(request, 'bottom.html', {
        'avg_cs': avg_cs,
        'avg_kda': avg_kda,
        'avg_gold': avg_gold,
        'avg_games_played': avg_games_played,
        'heroes': heroes,
        'win_rates': win_rates,
        'pick_rates': pick_rates
    })


def jungle(request):
    # 获取前五个英雄的名字
    top_heroes = list(
        loldata.objects.filter(role='打野', tier='challenger').order_by('id').values_list('hero', flat=True)[:5])

    # 使用这些英雄名字进行查询
    hero_statistics_data = hero_statistics.objects.filter(
        hero__in=top_heroes,
        tier='all',
        queue_type='ranked'
    )

    # 转换查询集为列表以便处理
    hero_statistics_list = list(hero_statistics_data.values('hero', 'win', 'pick'))

    # 提取数据
    heroes = [item['hero'] for item in hero_statistics_list]
    win_rates = [item['win'] for item in hero_statistics_list]
    pick_rates = [item['pick'] for item in hero_statistics_list]

    # 计算平均值
    avg_cs = hero_statistics_data.aggregate(Avg('cs'))['cs__avg']
    avg_kda = hero_statistics_data.aggregate(Avg('kda'))['kda__avg']
    avg_gold = hero_statistics_data.aggregate(Avg('gold'))['gold__avg']
    avg_games_played = hero_statistics_data.aggregate(Avg('games_played'))['games_played__avg']

    return render(request, 'jungle.html', {
        'avg_cs': avg_cs,
        'avg_kda': avg_kda,
        'avg_gold': avg_gold,
        'avg_games_played': avg_games_played,
        'heroes': heroes,
        'win_rates': win_rates,
        'pick_rates': pick_rates
    })


def middle(request):
    # 获取前五个英雄的名字
    top_heroes = list(
        loldata.objects.filter(role='中单', tier='challenger').order_by('id').values_list('hero', flat=True)[:5])

    # 使用这些英雄名字进行查询
    hero_statistics_data = hero_statistics.objects.filter(
        hero__in=top_heroes,
        tier='all',
        queue_type='ranked'
    )

    # 转换查询集为列表以便处理
    hero_statistics_list = list(hero_statistics_data.values('hero', 'win', 'pick'))

    # 提取数据
    heroes = [item['hero'] for item in hero_statistics_list]
    win_rates = [item['win'] for item in hero_statistics_list]
    pick_rates = [item['pick'] for item in hero_statistics_list]

    # 计算平均值
    avg_cs = hero_statistics_data.aggregate(Avg('cs'))['cs__avg']
    avg_kda = hero_statistics_data.aggregate(Avg('kda'))['kda__avg']
    avg_gold = hero_statistics_data.aggregate(Avg('gold'))['gold__avg']
    avg_games_played = hero_statistics_data.aggregate(Avg('games_played'))['games_played__avg']

    return render(request, 'middle.html', {
        'avg_cs': avg_cs,
        'avg_kda': avg_kda,
        'avg_gold': avg_gold,
        'avg_games_played': avg_games_played,
        'heroes': heroes,
        'win_rates': win_rates,
        'pick_rates': pick_rates
    })


def ranked_flex(request):
    return render(request, 'ranked_flex.html')


def ranked_solo(request):
    query = request.GET.get('search', '')  # 获取搜索框中的输入
    tier = request.GET.get('tier', '').lower()  # 段位
    role = request.GET.get('role', '')  # 位置

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
    # 分页
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
    # 获取前五个英雄的名字
    top_heroes = list(
        loldata.objects.filter(role='辅助', tier='challenger').order_by('id').values_list('hero', flat=True)[:5])

    # 使用这些英雄名字进行查询
    hero_statistics_data = hero_statistics.objects.filter(
        hero__in=top_heroes,
        tier='all',
        queue_type='ranked'
    )

    # 转换查询集为列表以便处理
    hero_statistics_list = list(hero_statistics_data.values('hero', 'win', 'pick'))

    # 提取数据
    heroes = [item['hero'] for item in hero_statistics_list]
    win_rates = [item['win'] for item in hero_statistics_list]
    pick_rates = [item['pick'] for item in hero_statistics_list]

    # 计算平均值
    avg_cs = hero_statistics_data.aggregate(Avg('cs'))['cs__avg']
    avg_kda = hero_statistics_data.aggregate(Avg('kda'))['kda__avg']
    avg_gold = hero_statistics_data.aggregate(Avg('gold'))['gold__avg']
    avg_games_played = hero_statistics_data.aggregate(Avg('games_played'))['games_played__avg']

    return render(request, 'support.html', {
        'avg_cs': avg_cs,
        'avg_kda': avg_kda,
        'avg_gold': avg_gold,
        'avg_games_played': avg_games_played,
        'heroes': heroes,
        'win_rates': win_rates,
        'pick_rates': pick_rates
    })


from django.db.models import Avg


def top(request):
    # 获取前五个英雄的名字
    top_heroes = list(
        loldata.objects.filter(role='上单', tier='challenger').order_by('id').values_list('hero', flat=True)[:5])

    # 使用这些英雄名字进行查询
    hero_statistics_data = hero_statistics.objects.filter(
        hero__in=top_heroes,
        tier='all',
        queue_type='ranked'
    )

    # 转换查询集为列表以便处理
    hero_statistics_list = list(hero_statistics_data.values('hero', 'win', 'pick'))

    # 提取数据
    heroes = [item['hero'] for item in hero_statistics_list]
    win_rates = [item['win'] for item in hero_statistics_list]
    pick_rates = [item['pick'] for item in hero_statistics_list]

    # 计算平均值
    avg_cs = hero_statistics_data.aggregate(Avg('cs'))['cs__avg']
    avg_kda = hero_statistics_data.aggregate(Avg('kda'))['kda__avg']
    avg_gold = hero_statistics_data.aggregate(Avg('gold'))['gold__avg']
    avg_games_played = hero_statistics_data.aggregate(Avg('games_played'))['games_played__avg']

    return render(request, 'top.html', {
        'avg_cs': avg_cs,
        'avg_kda': avg_kda,
        'avg_gold': avg_gold,
        'avg_games_played': avg_games_played,
        'heroes': heroes,
        'win_rates': win_rates,
        'pick_rates': pick_rates
    })


def analysis(request):
    # 查询 KDA、gold、cs 和 pick 排名前 7 的英雄
    top_kda_heroes = hero_statistics.objects.filter(tier="all", queue_type="ranked").order_by('-kda')[:7]
    top_gold_heroes = hero_statistics.objects.filter(tier="all", queue_type="ranked").order_by('-gold')[:7]
    top_cs_heroes = hero_statistics.objects.filter(tier="all", queue_type="ranked").order_by('-cs')[:7]
    top_pick_heroes = hero_statistics.objects.filter(tier="all", queue_type="ranked").order_by('-pick')[:7]

    # 提取英雄名字和对应的统计数据
    context = {
        'kda_hero_names': [hero.hero for hero in top_kda_heroes],
        'kdas': [hero.kda for hero in top_kda_heroes],

        'gold_hero_names': [hero.hero for hero in top_gold_heroes],
        'golds': [hero.gold for hero in top_gold_heroes],

        'cs_hero_names': [hero.hero for hero in top_cs_heroes],
        'css': [hero.cs for hero in top_cs_heroes],

        'pick_hero_names': [hero.hero for hero in top_pick_heroes],
        'picks': [hero.pick for hero in top_pick_heroes],
    }

    return render(request, 'analysis.html', context)


def analysis_hero(request, ):
    if request.method == 'POST':
        # 获取用户提交的英雄名
        hero_name = request.POST.get('heroName')

        # 查询该英雄在不同段位的胜率
        hero_data = hero_statistics.objects.filter(hero=hero_name, queue_type='ranked').order_by('tier')

        # 提取段位和胜率数据
        tiers = [data.tier for data in hero_data]
        win_rates = [data.win for data in hero_data]

        # 将数据传递给模板
        context = {
            'hero_name': hero_name,
            'tiers': tiers,
            'win_rates': win_rates,
        }
        return render(request, 'analysis_hero.html', context)

    # 处理 GET 请求，展示初始页面
    return render(request, 'analysis_hero.html')
