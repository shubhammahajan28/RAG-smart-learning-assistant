import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

def analyze_weakness(csv_path: str):
    df = pd.read_csv(csv_path)
    features = df[["correctness", "time_spent"]]
    scaled = MinMaxScaler().fit_transform(features)

    kmeans = KMeans(n_clusters=3, random_state=42)
    df["cluster"] = kmeans.fit_predict(scaled)

    # Low correctness + high time = weak topics
    weak = df[df["cluster"] == df.groupby("cluster")["correctness"].mean().idxmin()]
    weak_sorted = weak.sort_values("correctness").head(10)
    return weak_sorted[["domain", "topic", "correctness", "time_spent"]]