from sklearn.cluster import AgglomerativeClustering
import pandas as pd
import pickle

#클러스터링을 위해 pickle파일 불러오기
patient_sim_df = pd.read_pickle("patient_cosine_similarity_flatten.pkl")
problem_sim_df = pd.read_pickle("problem_cosine_similarity_flatten.pkl")


# 환자 기준 cosine similarity 결과 기반의 hierarchical clustering 을 통해 분류된 결과- 클러스터링 갯수 7
# ICF기준-> 주의력, 기억력, 집행력, 청각적 이해력, 말하기, 쓰기, 읽기
def patient_clustering_result_7():
    cluster_about_patient = AgglomerativeClustering(n_clusters=7,
                                                    affinity='euclidean',
                                                    linkage='ward')

    cluster_about_patient.fit(patient_sim_df)

    all_cluster_about_patient = []
    cluster1 = []
    cluster2 = []
    cluster3 = []
    cluster4 = []
    cluster5 = []
    cluster6 = []
    cluster7 = []

    index = 0
    for i in range(len(cluster_about_patient.fit_predict(patient_sim_df))):
        if cluster_about_patient.fit_predict(patient_sim_df)[i] == 0:
            cluster1.append(index)
        elif cluster_about_patient.fit_predict(patient_sim_df)[i] == 1:
            cluster2.append(index)
        elif cluster_about_patient.fit_predict(patient_sim_df)[i] == 2:
            cluster3.append(index)
        elif cluster_about_patient.fit_predict(patient_sim_df)[i] == 3:
            cluster4.append(index)
        elif cluster_about_patient.fit_predict(patient_sim_df)[i] == 4:
            cluster5.append(index)
        elif cluster_about_patient.fit_predict(patient_sim_df)[i] == 5:
            cluster6.append(index)
        else:
            cluster7.append(index)
        index += 1
    all_cluster_about_patient.append(cluster1)
    all_cluster_about_patient.append(cluster2)
    all_cluster_about_patient.append(cluster3)
    all_cluster_about_patient.append(cluster4)
    all_cluster_about_patient.append(cluster5)
    all_cluster_about_patient.append(cluster6)
    all_cluster_about_patient.append(cluster7)

    return all_cluster_about_patient


patient_cluster_series = patient_clustering_result_7()

with open("patient_cluster_series.pkl","wb") as f:
    pickle.dump(patient_cluster_series, f)




# 문항 기준 cosine similarity 결과 기반의 hierarchical clustering 을 통해 분류된 결과- 클러스터링 갯수 7
# ICF기준-> 주의력, 기억력, 집행력, 청각적 이해력, 말하기, 쓰기, 읽기
def problem_clustering_result_7():
    cluster_about_problem = AgglomerativeClustering(n_clusters=7,
                                                    affinity='euclidean',
                                                    linkage='ward')

    cluster_about_problem.fit(problem_sim_df)

    all_cluster_about_problem = []
    cluster1 = []
    cluster2 = []
    cluster3 = []
    cluster4 = []
    cluster5 = []
    cluster6 = []
    cluster7 = []

    index = 0
    for i in range(len(cluster_about_problem.fit_predict(problem_sim_df))):
        if cluster_about_problem.fit_predict(problem_sim_df)[i] == 0:
            cluster1.append(index)
        elif cluster_about_problem.fit_predict(problem_sim_df)[i] == 1:
            cluster2.append(index)
        elif cluster_about_problem.fit_predict(problem_sim_df)[i] == 2:
            cluster3.append(index)
        elif cluster_about_problem.fit_predict(problem_sim_df)[i] == 3:
            cluster4.append(index)
        elif cluster_about_problem.fit_predict(problem_sim_df)[i] == 4:
            cluster5.append(index)
        elif cluster_about_problem.fit_predict(problem_sim_df)[i] == 5:
            cluster6.append(index)
        else:
            cluster7.append(index)
        index += 1
    all_cluster_about_problem.append(cluster1)
    all_cluster_about_problem.append(cluster2)
    all_cluster_about_problem.append(cluster3)
    all_cluster_about_problem.append(cluster4)
    all_cluster_about_problem.append(cluster5)
    all_cluster_about_problem.append(cluster6)
    all_cluster_about_problem.append(cluster7)

    return all_cluster_about_problem


problem_cluster_series = problem_clustering_result_7()

with open("problem_cluster_series.pkl","wb") as f:
    pickle.dump(problem_cluster_series, f)