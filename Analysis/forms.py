# forms.py
from django import forms

class WizardForm(forms.Form):
    ROLE_CHOICES = [
        ('上单', '上路'),
        ('中路', '中路'),
        ('打野', '打野'),
        ('射手', '射手'),
        ('辅助', '辅助'),
    ]
    QUEUE_TYPE_CHOICES = [
        ('solo', '单排'),
        ('team', '组排'),
    ]
    TIER_CHOICES = [
        ('坚韧黑铁', '坚韧黑铁'),
        ('英勇黄铜', '英勇黄铜'),
        ('不屈白银', '不屈白银'),
        ('荣耀黄金', '荣耀黄金'),
        ('华贵铂金', '华贵铂金'),
        ('流光翡翠', '流光翡翠'),
        ('璀璨钻石', '璀璨钻石'),
        ('超凡大师', '超凡大师'),
        ('傲世宗师', '傲世宗师'),
        ('最强王者', '最强王者'),
    ]
    REMARK_CHOICES = [
        ('糕手', '糕手'),
        ('高手', '高手'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, label='你想玩哪路？')
    queue_type = forms.ChoiceField(choices=QUEUE_TYPE_CHOICES, label='你是单排还是组排')
    tier = forms.ChoiceField(choices=TIER_CHOICES, label='你的段位')
    remark = forms.ChoiceField(choices=REMARK_CHOICES, label='你自认为操作如何', required=False)
