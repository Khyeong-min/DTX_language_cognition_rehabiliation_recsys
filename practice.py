import pandas as pd
import pickle

# 리스트 pickle파일로 저장된 것 출력(예시)
with open("problem_cluster_series.pkl", "rb") as f:
    problem_cluster_series_load = pickle.load(f)
print(problem_cluster_series_load)


# 데이터프레임 pickle파일로 저장된 것 출력(예시)
final_df_for_clustering_algorithm = pd.read_pickle("final_df_for_clustering_algorithm.pkl")
print(final_df_for_clustering_algorithm.loc['39af54']['인지-주의력-패턴 따라하기-3'])






