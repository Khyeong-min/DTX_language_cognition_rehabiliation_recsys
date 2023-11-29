import pandas as pd


#클러스터링을 위해 pickle파일 불러오기
final_df_for_clustering_algorithm = pd.read_pickle("final_df_for_clustering_algorithm.pkl")
patient_cluster_series = pd.read_pickle("patient_cluster_series.pkl")


# 환자번호가 들어올 때 본인이 속한 클러스터를 찾는 함수
def extract_cluster(patientCode):
    cluster_index = 0
    for patient_code in final_df_for_clustering_algorithm.index:
        if patient_code == patientCode:
            for cluster in patient_cluster_series:
                if cluster_index in cluster:
                    return cluster
        else:
            cluster_index += 1


# 본인이 푼 문항 리스트를 추출
def my_problem_list(PatientCode):
    my_problem_index = []
    cnt = 0
    for column in final_df_for_clustering_algorithm.columns:
        if final_df_for_clustering_algorithm.loc[PatientCode][column] != [-1.0, -1.0]:
            my_problem_index.append(cnt)
        cnt += 1

    return my_problem_index


# 클러스터의 해당 문제에 대한 평균시간을 구하는 함수
def average_time_from_cluster(extracted_cluster_index, each_problem_index):
    sum_time = 0.
    for cluster_index in extracted_cluster_index:
        if final_df_for_clustering_algorithm.iloc[cluster_index, each_problem_index] != ([-1.0, -1.0]):
            sum_time += float(final_df_for_clustering_algorithm.iloc[cluster_index, each_problem_index][1])
    sum_time /= len(extracted_cluster_index)

    return sum_time


# 클러스터의 해당 문제에 대한 평균 정답률을 구하는 함수
def average_corect_from_cluster(extracted_cluster_index, each_problem_index):
    sum_correct = 0.
    for cluster_index in extracted_cluster_index:
        if final_df_for_clustering_algorithm.iloc[cluster_index, each_problem_index] != ([-1.0, -1.0]):
            sum_correct += float(final_df_for_clustering_algorithm.iloc[cluster_index, each_problem_index][0])
    sum_correct /= len(extracted_cluster_index)

    return sum_correct


# 클러스터 내에 환자들이 푼 문항 중 내가 풀지 않은 문항의 인덱스 번호를 추출
def rec_system_1(PatientCode):
    # 클러스터 뽑기
    extracted_cluster_index = extract_cluster(PatientCode)

    # 내가 푼 문항을 뽑기
    problem_list = my_problem_list(PatientCode)

    # 클러스터 내에서 환자가 푼 문제와 내가 푼 문제를 비교
    cluster_problem_index = []
    for cluster_index in extracted_cluster_index:
        problem_list2 = my_problem_list(final_df_for_clustering_algorithm.index[cluster_index])
        for problem_index in list(problem_list2):
            cluster_problem_index.append(problem_index)
    cluster_problem_index_fixed = list(set(cluster_problem_index))

    for problem_index in cluster_problem_index_fixed:
        if problem_index in cluster_problem_index:
            cluster_problem_index.remove(problem_index)

    # 클러스터에서 푼 문제 중에 내가 풀지 않은 문제들 전달
    final_problem_list_1 = list(set(cluster_problem_index) - set(problem_list))

    return final_problem_list_1


def rec_system_2(PatientCode):
    # 최종리스트
    final_problem_list_2 = []

    # 클러스터 뽑기
    extracted_cluster_index = extract_cluster(PatientCode)

    # 내가 푼 문항을 뽑기
    problem_index_list = my_problem_list(PatientCode)

    # 내가 푼 문항을 반복돌리기
    for each_problem_index in problem_index_list:
        column_value = final_df_for_clustering_algorithm.columns[each_problem_index]
        column_value_for_comparison = final_df_for_clustering_algorithm.columns[each_problem_index + 1]
        # 문제의 정답률이 80% 이상
        if float(final_df_for_clustering_algorithm.loc[PatientCode][column_value][0]) >= 0.8:
            # 현재의 난이도가 최대 X
            if (column_value[:-2] == column_value_for_comparison[:-2]):
                final_problem_list_2.append(each_problem_index + 1)

            # 현재의 난이도가 최대 O
            else:
                average_time = average_time_from_cluster(extracted_cluster_index, each_problem_index)
                if float(final_df_for_clustering_algorithm.loc[PatientCode][column_value][1]) > average_time:
                    final_problem_list_2.append(each_problem_index)

                else:
                    pass
        # 문제의 정답률이 80% 이하
        else:
            average_corrected = average_corect_from_cluster(extracted_cluster_index, each_problem_index)
            if float(final_df_for_clustering_algorithm.loc[PatientCode][column_value][0]) > average_corrected:
                final_problem_list_2.append(each_problem_index)

            else:
                final_problem_list_2.append(each_problem_index - 1)

    return final_problem_list_2
