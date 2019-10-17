from collections import Counter
from django.shortcuts import render_to_response

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся
counter_show = Counter()
counter_click = Counter()

def index(request):

    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    x = request.GET.get('from-landing')
    if x == 'original':
        counter_click.update(x.split())
        print(counter_click)
        return render_to_response('landing.html')
    elif x == 'test':
        counter_click.update(x.split())
        print(counter_click)
        return render_to_response('landing_alternate.html')
    else:
        return render_to_response('index.html')

def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    x = request.GET.get('ab-test-arg')
    if x == 'original':
        counter_show.update(x.split())
        print(counter_show)
        return render_to_response('landing.html')
    elif x == 'test':
        counter_show.update(x.split())
        print(counter_show)
        return render_to_response('landing_alternate.html')

def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Чтобы отличить с какой версии лендинга был переход
    # проверяйте GET параметр marker который может принимать значения test и original
    # Для вывода результат передайте в следующем формате:
    #print('click: ', click, 'show: ', show)

    click_test = dict(counter_click).get('test')
    click_original = dict(counter_click).get('original')
    print('click_test: ', click_test, 'click_original: ', click_original)

    show_test = dict(counter_show).get('test')
    show_original = dict(counter_show).get('original')
    print('show_test: ', show_test, 'show_original: ', show_original)

    try:
        test_conversion = round(click_test / show_test, 2)
    except TypeError:
        test_conversion = 0

    try:
        original_conversion = round(click_original / show_original, 2)
    except TypeError:
        original_conversion = 0

    return render_to_response('stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
