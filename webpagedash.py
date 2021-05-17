import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.exceptions import PreventUpdate
import dash_html_components as html
from dash.dependencies import Input, Output
import re
from bs4 import BeautifulSoup
import requests

app = dash.Dash(__name__)
server = app.server


app.layout = html.Div(
    [
        html.H1("Input the url to get the name and the address or info",
            style = {
                'margin-left': '26%',
                'color':'#0A3E7C',
                'font-family':'cursive'
            }),
        dcc.Input(
            id="input",
            type="text",
            placeholder="input the url",
            style = {
                'margin-left':'40%',
                'margin-top':'3%',
                'color':'#1A3E5C',
                'font-family':'cursive'
            }
        ),
        html.Br(),
        html.Br(),


        html.H5("Name & address:",
            style = {

                'margin-left':'35%',
                'margin-top':'1%',
                'color':'#663300',
                'font-family':'Helvetica',
                'float':'left'

            }),


        html.H5(
            id="out",
            style = {
                'margin-left':'42%',
                'margin-top':'1%',
                'color':'#663300',
                'font-family':'Helvetica',

            }),



        html.H5(
            id="out1",
            style = {
                'margin-left':'42%',
                'margin-top':'1%',
                'color':'#0000b3',
                'font-family':'Helvetica'
            }),


],
    style = {
                "background-color": "coral"
            },
)


@app.callback(
    Output("out", "children"),Output("out1", "children"),
    Input("input", "value"),
)

def converter(url):
    if url is None:
        raise PreventUpdate
    else:
        try:
            response0 = requests.get(url)

        except requests.exceptions.RequestException:
            return "", "Their is no such website, please write a valid website with full name including 'https://'"
        b= re.findall(r'(\w+)', f"{url}")
        c =b[1:-1]
        if len(c)==2:
            f =c[1]
        elif len(c)==1:
            f= c[0]
        response= requests.get(f'https://www.google.com/search?q={f}')
        if response.status_code <300:
            page = response.content
            bpage = BeautifulSoup(page,'html.parser')
            address =bpage.find_all("span", class_ ="BNeawe tAd8D AP7Wnd")
            a = [i.get_text() for i in address][:2]
            name =bpage.find_all("div", class_ ="BNeawe vvjwJb AP7Wnd")
            n= [i.get_text() for i in name][0]
            return  n, " ".join(a)
        else:
            return "","We cant extract info from that website"



if __name__ == "__main__":
    app.run_server(debug=True)
