# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all
#     notebook_metadata_filter: all,-language_info
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
from base64 import b64encode
from io import BytesIO

import markupsafe
import jinja2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# -

# Monkeypatch DataFrame so that instances can display charts in a notebook
pd.DataFrame._repr_html_ = lambda self: self.to_html(escape=False)

table = pd.DataFrame(np.random.randint(0, 100, size=(4, 10)))

table

# +
charts = pd.DataFrame(index=table.index, columns=["chart"])

for ix, series in table.iterrows():
    plt.plot(series)
    buf = BytesIO()
    plt.savefig(buf)
    plt.close()
    charts.loc[ix]["chart"] = '<img src="data:image/png;base64,{}"/>'.format(b64encode(buf.getvalue()).decode())
# -

charts


# Trust me on this...
def df_to_html(df):
    return markupsafe.Markup(df.to_html(escape=True)).unescape()


# +
with open("../template.html") as f:
    template = jinja2.Template(f.read())

context = {
    "title": "Template demo",
    "table": df_to_html(table),
    "charts": df_to_html(charts),
}

with open("../output.html", "w") as f:
    f.write(template.render(context))
