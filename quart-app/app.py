from quart import Quart, render_template, request

app = Quart(__name__)


@app.route("/api/brig")
async def brig():
    # rank, Name, Number, Branch, console, position, company, platoon, class, TiS
    return jsonify(
        {
            "rank": "PFC",
            "Name": "John Doe",
            "Number": "123456",
            "Branch": "Army",
            "console": "PC",
            "position": "Rifleman",
            "company": "A",
            "platoon": "1",
            "class": "1",
            "TiS": "1",
        }
    )
