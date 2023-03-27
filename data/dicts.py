from collections import OrderedDict

FORMS = ("1s", "1m", "2ms", "2fs", "2mm", "2fm", "3ms", "3fs", "3mm", "3fm")

PERSONAL_PRONOUNS_HE = OrderedDict(
    [
        ("1s", "אני"),
        ("1m", "אנחנו"),
        ("2ms", "אתה"),
        ("2fs", "את"),
        ("2mm", "אתם"),
        ("2fm", "אתן"),
        ("3ms", "הו"),
        ("3fs", "הי"),
        ("3mm", "הם"),
        ("3fm", "הן"),
    ]
)
PERSONAL_PRONOUNS_RU = OrderedDict(
    [
        ("1s", "Я"),
        ("1m", "Мы"),
        ("2ms", "Ты (м.р.)"),
        ("2fs", "Ты (ж.р.)"),
        ("2mm", "Вы (м.р.)"),
        ("2fm", "Вы (ж.р.)"),
        ("3ms", "Он"),
        ("3fs", "Она"),
        ("3mm", "Они (м.р.)"),
        ("3fm", "Они (ж.р.)"),
    ]
)
