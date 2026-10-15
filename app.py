
from flask import Flask, request, jsonify, render_template_string
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Load dataset and train the ML model
iris = load_iris()
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(iris.data, iris.target)

FLOWERS = iris.target_names.tolist()

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FloraAI | ML Prediction</title>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Arial,sans-serif;background:#f3f6fb;color:#17243b}
header{padding:22px 8%;background:#fff;border-bottom:1px solid #e3e8f0}
.brand{font-size:23px;font-weight:bold;color:#177d70}
main{max-width:850px;margin:55px auto;padding:0 20px}
.hero{text-align:center;margin-bottom:30px}
.hero h1{font-size:36px;margin-bottom:10px}
.hero p{color:#64748b;line-height:1.6}
.card{background:white;border:1px solid #e3e8f0;border-radius:18px;
padding:28px;box-shadow:0 12px 35px #1527470c}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px}
label{display:block;font-size:14px;font-weight:bold;margin-bottom:9px}
input{width:100%;padding:13px;border:1px solid #d5dce7;
border-radius:9px;font-size:16px}
button{width:100%;margin-top:24px;padding:15px;border:0;
border-radius:9px;background:#177d70;color:white;font-size:16px;
font-weight:bold;cursor:pointer}
button:hover{background:#11695f}
#result{display:none;margin-top:22px;padding:20px;background:#e9f7f2;
border-radius:12px;color:#17654e;text-align:center}
#result h2{margin:8px 0;text-transform:capitalize}
footer{text-align:center;color:#7a8799;padding:28px;font-size:13px}
@media(max-width:550px){.grid{grid-template-columns:1fr}.hero h1{font-size:29px}}
</style>
</head>
<body>
<header><div class="brand">🌿 FloraAI</div></header>
<main>
<section class="hero">
<h1>Flower Classification</h1>
<p>Enter four flower measurements and let our
Machine Learning model predict the species.</p>
</section>
<section class="card">
<form id="form">
<div class="grid">
<div><label>Sepal length (cm)</label>
<input name="a" type="number" step="any" min="0" max="10" value="5.1" required></div>
<div><label>Sepal width (cm)</label>
<input name="b" type="number" step="any" min="0" max="10" value="3.5" required></div>
<div><label>Petal length (cm)</label>
<input name="c" type="number" step="any" min="0" max="10" value="1.4" required></div>
<div><label>Petal width (cm)</label>
<input name="d" type="number" step="any" min="0" max="10" value="0.2" required></div>
</div>
<button type="submit">Predict Flower Species →</button>
</form>
<div id="result" role="status"></div>
</section>
</main>
<footer>FloraAI · Python · Scikit-learn · Flask · Docker · AWS</footer>
<script>
document.getElementById('form').addEventListener('submit',async e=>{
 e.preventDefault();
 const f=new FormData(e.target);
 const features=['a','b','c','d'].map(k=>Number(f.get(k)));
 const box=document.getElementById('result');
 box.style.display='block';
 box.textContent='Analysing measurements...';
 try{
  const r=await fetch('/predict',{method:'POST',
   headers:{'Content-Type':'application/json'},
   body:JSON.stringify({features})});
  const data=await r.json();
  if(!r.ok) throw new Error(data.error||'Prediction failed');
  box.innerHTML='<div>Predicted species</div><h2></h2><div>ML prediction completed successfully.</div>';
  box.querySelector('h2').textContent=data.prediction;
 }catch(err){box.textContent='Error: '+err.message;}
});
</script>
</body>
</html>
"""


@app.get("/")
def home():
    return render_template_string(HTML)


@app.post("/predict")
def predict():
    data = request.get_json(silent=True) or {}
    features = data.get("features")

    if not isinstance(features, list) or len(features) != 4:
        return jsonify({
            "error": "Provide exactly four numeric features."
        }), 400

    try:
        values = [float(x) for x in features]
        if any(not 0 <= x <= 10 for x in values):
            raise ValueError()
    except (TypeError, ValueError):
        return jsonify({
            "error": "Each feature must be a number between 0 and 10."
        }), 400

    prediction = int(model.predict([values])[0])
    probabilities = model.predict_proba([values])[0]

    return jsonify({
        "prediction": FLOWERS[prediction],
        "confidence": round(float(max(probabilities)) * 100, 2),
        "model": "RandomForestClassifier"
    })


@app.get("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
