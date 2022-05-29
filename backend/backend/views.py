from turtle import home
from django.shortcuts import render, redirect
from .db_access import get_conn, get_speech_segments, get_phrases, get_table_values

# Create your views here.
# Create your views here.
def homeview(request):
    # establish the connection with the db
    conn = get_conn()

    # get the values from the db itself
    speech_segments = get_speech_segments(conn)

    # data for the home page specifically
    home_data = []

    ss = []
    for segment in speech_segments:
        t = []
        home_t = []
        for ind, val in enumerate(segment):
            t.append(val)
            if ind != 2:
                home_t.append(val)
        ss.append(t)
        home_data.append(home_t)
    speech_segments = ss

    print(speech_segments)


    context = {
        'msg': 'hello world',
        'home_data': home_data,
        'speech_segments': speech_segments,
    }
    return render(request, "backend/home.html", context)


def protected_view(request, pk):
    # establish the connection with the db
    conn = get_conn()

    # get the values from the db itself
    speech_segments = get_speech_segments(conn)

    # data for the home page specifically
    protected_view_data = []
    full_text = {}

    for segment in speech_segments:
        for ind, val in enumerate(segment):
            if ind == 2:
                full_text[segment[0]] = val

    phrases = get_phrases(conn, pk)

    pv = []
    for phrase in phrases:
        tmp = []
        if phrase:
            tmp.append(phrase[0])
            tmp.append(phrase[2])
            tmp.append(f'{phrase[3]} ({phrase[4]})')
            pv.append(tmp)
    protected_view_data = pv

    ft = full_text[pk]

    context = {
        'pk': pk,
        'phrases': phrases,
        'full_text': ft,
        'protected_view_data': protected_view_data,
    }
    return render(request, "backend/protected.html", context)
    pass
