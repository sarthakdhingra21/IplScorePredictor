import streamlit as st
import numpy as np
import joblib
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb


def image(link,src_as_string, **style):
    return a(_href=link, _target="_blank")(img(src=src_as_string, style=styles(**style)))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="white",
        text_align="center",
        height="auto",
        opacity=1
    )
    style_div: link(
            color="white"
            )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    
    myargs = [
        "Connect: ",
        image("https://github.com/sarthakdhingra21",'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOAAAADgCAMAAAAt85rTAAAAkFBMVEX///8XFRUAAAAUEhIPDAwLCAjq6uoRDw8KBgb6+voGAADR0dHx8fHc3NzW1tYVEhLLysrm5uZFRERcW1vAwMBVVFS2trZwb29paGhkY2OlpKTa2tqysrKZmZnv7+92dXU7OjoeHBwxLy89PDwoJiZKSUmNjY2dnJyBgICqqak2NDTEw8MkIiJ0dHSJiIh9fX2ZaVQFAAAKVklEQVR4nO1daXerNhANAxjwvuEtJo7XxM6r/f//XcHYDTZoRqAFt9X90PNO44O4aKRZNXp7MzAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDB4IbQb3cnXebbf+HCDdQpX0WI8+AjqfjdhtJarcHcl1XQ920ph217K1f8cHcaDut+xKto/h8+EhetZLNyIzhedf91UDhahB+AwqT3QbAJspuN/EcdBFEulb9PUfuElEzlp1/3mPAiOewC2VCJoQm/aqvv1KXRX8aKrwu6KXrzBLj7q5oBgHMZvKAYP3O9G3TwYmOzAF6SXwAaYvdfNpQCTz2orrwgA01fTjv0Tp07gpnh5JUFtzOXSSyl+1U3rjiCCpmx6VrIW1/26qV3R3YjunCx4MH0B82YlXzp/ATCumd77SdX0pbDhUiu/L5XTlwLWndroBXO105fCgWNN/DprHfwSMV3Vwu9HvXjeAcMadtMISjl8ggwt7QvxrEc873BAs6eoZXvJwoPJf5pf4gxrZLjXzy/ZTLWpi1Ed/GLomsOwJn66GK5q4xdLqQYH6rs+fgnDrmp+xzr5xfrQVRwc/qmXn2X5J6VW24dO+6wYMFPILzhVj1rLYxipIzgtFlD3muuTFhWNYTtporTwb+rM0iWD3/64XJxHG950GYVeTG04jY7LqHg8DxQtwwFjAd6+aNBZbCvmlbLwAabjW9CXITGqluFncebB2f7+pBFtxKYRIMxYK33Gnq3GKv1ijXbO/iqYbKrnz+LJe0i7tNfFMmODAm3YYWmI3JofD6smQHP5CIaMWs1QPsEhKzUG+d9OrKev0fPcJmTR9B2v9/ATB0b5sARjW1NhdjNNNGdY9PPfdEWSfQfnFM7/OkTHyTjGchF9z0bDa3WJf2cJ2yI7usMa1Za9kwZrltQ9LsF/0AjB85JZ260YFT/txvsyCq+FJnaTpb2ZliF8S2T3hvkQzB1t7KznC1onN37OewhZifkTczWD1Dhbg21js120NvdWx851zpiJObn7zAwhqDTZfKjyZcvjHXGSQGmqmWGtJXD38oYZsTO4dlNpXcsC+7Q/skZhbtb1EszaiGJAVmBs+isVUZZ9mE6hpFXI8iJuo9S1BuONdC5nEDyOpjbOdcHHlqML8TiM2mDsEHW+5JgzRKAQDjIGYYEI4kmxSPe4e+cq8Fz+wYAiuBQfA9MR6SDiYzDBdJfuX1eCskeMpRtBafo2jzlVIybBUCRDvTCVwKQYdJxZPEjapSbQU6kIMUMmHX0nOgRVbKA434PrQUuCKtwSUUBYSCHCxJAI0YmOT+2hMJLDg4kGsQxFtRSh5Xu+8sJjYhn2BBOGI7yOXkfhAyGkgloK/3yeJYkEBlb8/k5QyFQklISeqgfcVvQ2Is/Gl6DYs7lBTaHIs1m5gdujFauIO3BVJeTXE+6YpuNwaNxCaKP7aGJKyFfpKGWBhJ0tMVsYV/P6iuN2WDpOxGXC3TG1Me0sUJfNXldfKWhMy1NbkpMFXn4k4M5MMX+zqbIi5xHEIqy+jX5im6jaaNMDgg22CAUCM3jEV+OxohAzZgS8elWSURrsNKElEh0lRF/jUQY0uO5XjuATalDjGVRUTxSXQfCghRPU2LcA11d/qj4WN+N1EkStUbuyPzHGCWpsWYDOYHWHiSD4KmtQGcFX2UWVEVRe4f+Lv2ohqFHR40kYVQRfxVSrTpDwUvS1YghQq786QUIPSq73Q9Be95AXsZtVn4tbMr7qtMQv8Ex29eglbovKKzQigYtSdVv0A32urc+UweOGAvVAREhZ28FoIv5cXHPMAzQsqnEbxXu0CbwHvjtr22Vwx1skJkOcZlVZIZMFUS0jsFRwL0WbsUZUywi4NROCoJ4uIW0PXYLerrrnTZQgeH+0xLaJzyySm2hbeImDHnubqAYUkiM8P2i5lW2IEiArDkWSXLijqcfpJd9BxN6gyhllVU0jwCvGLUFlRReLKtcUVGeX6qb2FRRBR3WhBe6yWcJJLjTrcX2+wlPtb0nijDoSLChDZOsKW230kGwNYvfEAuzUHh0Lqa1Q2xM63pJg8ROa0FJaUflOt84QLvUg7O3rGKqS9QOO09zCCQSyZttSZnQP/tA9BySUyzFPJ2cZqqh5avH0VJBQLscho0nzQemppiNP65qehGIkeh9N4EouHW3PuFrzSIma4HmBO2yYS8z4jjk7e0r5rHgKJjMYHCRpxC5vM4zqyesHPAvLrR1FfmJhHUmg2B1xtzMRiIhm8bTNwHfsBAbdRZjvru0BrMTa1H8sN/wN821J9Y6PZzN67v3/d+YFkgSwjapyDCYzt0y/HWne6GN49O5BT77e+ruC9ekA+JfJoKSwfvSjLQAeSs99TFmXGjxqCu/WjnYVe2JBcSPOpO3UaR6N+RyNQX8xHfrlW15JbIXwmPzwbrHy9yD3p+yv0g45J8ICOKQ7llOhIZ3E5M9z5AJGqc5rjFpEM046sFi5mafUmvjnY3yQ+tFdgDZ6togn8XOq2MZL2gpM0H7+zF56Jmqxb2O2nPPJ8Wwy6sLgJzeglzO5M71M2Qfg+FYJ1iqDCVk68I4gd3TBu2Wwx623LUNIOVcJ1q2GCekV43mL1E+LEABarFOavKmLsPxlP15PMr+i3S6NGA5jf54RAOc1hSt0nVWQ9mn4uWKc6zIIogGjDILbkiJS1EX8VJzdz+8lmWhTUWt//nCCgxUyFUBJb8NCIb0lly7neI0y/0oDLxPJQ1FespEzhW9C2AYYJXcvZZwL2wXYc39mrrhPhp+q5hL5nfQWlfxOLJq3zuXPtS/j9T/7rxJ6isrSPcJZK+JX0Hjhro1aqTTGbvBhOrscFv1yVV6lmlsrbS6xf3LibftXDPsPl3kthzN+j5Anuvz7USU0yWGi/ezDZ65Figkmxk3/tIsS/wNKnOAn86zZEdV1d0nQzUWgftNz3Sj59yqmFgvrOSwRcy5BUEkQPYvnhJZtP20mwfGrdJSbn6DbU16a87ylO4541J7b3PY8DeeGn7dSdy28q/ES1HAbQ4Jnu8MTLhzlJNjTVf2X81CLOxDzg4+gre+kRo6hA5ulwFLkItjTeRIlbx17AOHh574FBJ3+Ysqf2eYhaKvs35ZHQbcsO72C3V2vb9kZ/hIkDkvG0303GPNuNzvG9R8Of+CZDqz5Og/zpVhSKViZBGFbw628LSLPVaJKjiIIYS23uTaGsk7c4ARtjU0lnjDFxFQWQV/vxXyPmCDZZkkEYVjrBfWDLXMSnS33wmGfLnPqE887DqxJLHH8jkkQTpq1XxE6jEkUJ+hKqqIQxtEpesESLZEKCdowrO8O5Sd8rAoubC9BsCCqZkOdm2cenXluKQoRBJBRUyQV/e2TZVOdYDx73zWYZiT64UN+wttUIxjTO9eq+hC0Zpn8RAlFn3GX3Fg4X3H27mgcdndJLaGig51zn7z9S20tRQjGo+RiLB/KVFP/APjJLYbnl1EMKILjPByVK6YeXMLworG9iYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYHB/xJ/A+HljiNdQqEOAAAAAElFTkSuQmCC',
              width=px(25), height=px(25)),
        image("https://www.linkedin.com/in/sarthakdhingra21","data:image/png;base64,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",width=px(25), height=px(25)),
        br(),
    ]
    layout(*myargs)

ipl_model=open("first-innings-score-lr-model.pkl","rb")
ipl_m=joblib.load(ipl_model)

def predict_score(batting_team,bowling_team,overs,runs,wickets,runs_in_prev_5,wickets_in_prev_5):
    temp_array = list()
    
    
    if batting_team == 'Chennai Super Kings':
        temp_array = temp_array + [1,0,0,0,0,0,0,0]
    elif batting_team == 'Delhi Daredevils':
        temp_array = temp_array + [0,1,0,0,0,0,0,0]
    elif batting_team == 'Kings XI Punjab':
        temp_array = temp_array + [0,0,1,0,0,0,0,0]
    elif batting_team == 'Kolkata Knight Riders':
        temp_array = temp_array + [0,0,0,1,0,0,0,0]
    elif batting_team == 'Mumbai Indians':
        temp_array = temp_array + [0,0,0,0,1,0,0,0]
    elif batting_team == 'Rajasthan Royals':
        temp_array = temp_array + [0,0,0,0,0,1,0,0]
    elif batting_team == 'Royal Challengers Bangalore':
        temp_array = temp_array + [0,0,0,0,0,0,1,0]
    elif batting_team == 'Sunrisers Hyderabad':
        temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
    if bowling_team == 'Chennai Super Kings':
        temp_array = temp_array + [1,0,0,0,0,0,0,0]
    elif bowling_team == 'Delhi Daredevils':
        temp_array = temp_array + [0,1,0,0,0,0,0,0]
    elif bowling_team == 'Kings XI Punjab':
        temp_array = temp_array + [0,0,1,0,0,0,0,0]
    elif bowling_team == 'Kolkata Knight Riders':
        temp_array = temp_array + [0,0,0,1,0,0,0,0]
    elif bowling_team == 'Mumbai Indians':
        temp_array = temp_array + [0,0,0,0,1,0,0,0]
    elif bowling_team == 'Rajasthan Royals':
        temp_array = temp_array + [0,0,0,0,0,1,0,0]
    elif bowling_team == 'Royal Challengers Bangalore':
        temp_array = temp_array + [0,0,0,0,0,0,1,0]
    elif bowling_team == 'Sunrisers Hyderabad':
        temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
    overs = float(overs)
    runs = int(runs)
    wickets = int(wickets)
    runs_in_prev_5 = int(runs_in_prev_5)
    wickets_in_prev_5 = int(wickets_in_prev_5)
        
    temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]
        
    data = np.array([temp_array])
    my_prediction = int(ipl_m.predict(data)[0])
    return my_prediction

def main():
    st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        padding-top: 0rem;
    }}
</style>
""",
        unsafe_allow_html=True,
    )
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
     
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    footer()
    st.title("IPL'21 Score Predictor")
    from PIL import Image
    img=Image.open("img.webp")
    img.resize((round(img.size[0]*0.5), round(img.size[1]*0.8)))
    st.image(img,use_column_width=True)
    st.sidebar.header("About us")
    st.sidebar.text("This is a Machine Learning Web App which is \nintegrated with a model built using \nkaggle dataset of previous ipl years")
    st.sidebar.text("You can predict the final first innings \nscore with few clicks " )
    batting_team=st.sidebar.selectbox("Select your batting team",('Chennai Super Kings','Delhi Daredevils','Kings XI Punjab','Kolkata Knight Riders','Mumbai Indians','Rajasthan Royals','Royal Challengers Bangalore','Sunrisers Hyderabad'))
    bowling_team=st.sidebar.selectbox("Select your bowling team",('Chennai Super Kings','Delhi Daredevils','Kings XI Punjab','Kolkata Knight Riders','Mumbai Indians','Rajasthan Royals','Royal Challengers Bangalore','Sunrisers Hyderabad'))
    overs=st.slider("Enter numbers of overs",min_value=0,max_value=20,step=1)
    runs=st.text_input("Enter numbers of runs ")
    wickets=st.radio("Select Number of wickets fallen",(0,1,2,3,4,5,6,7,8,9,10))
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    runs_in_prev_5=st.text_input("Enter runs scored in prev 5 balls")
    wickets_in_prev_5=st.text_input("Enter wickets in prev 5 balls")
    if(st.button("Predict the score")):
        result=predict_score(batting_team,bowling_team,overs,runs,wickets,runs_in_prev_5,wickets_in_prev_5)
        st.success("Predicted score is "+str(result))
    
if __name__=='__main__':
    main()