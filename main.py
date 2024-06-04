from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Читаем CSV файл
df = pd.read_csv('data.csv', delimiter='\t')


def filter_data(df, **filters):
    for key, value in filters.items():
        if value is not None and value != '':
            df = df[df[key].astype(str).str.contains(str(value))]
    return df


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/filter", response_class=HTMLResponse)
def filter_dataset(
    request: Request,
    d_z: str = Query(None),
    short_name: str = Query(None)
):
    filters = {
        'd_z': d_z,
        'short_name': short_name
    }
    filtered_df = filter_data(df, **filters)
    return filtered_df.to_html(index=False, classes="table table-striped")


@app.get("/filters")
def get_filters():
    d_z_values = df['d_z'].unique().tolist()
    short_name_values = df['short_name'].unique().tolist()
    return {"d_z": d_z_values, "short_name": short_name_values}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
